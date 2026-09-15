"""
Standalone Crypto Signal Engine — independent of equities and options, same
account. Daily bars (see crypto_signals.py for why).

Reuses strategy/indicators.py (compute_all) and strategy/signals.py
(generate_signal) verbatim -- both are ticker-agnostic pandas functions, no
crypto-specific reimplementation needed. BTC plays the role SPY plays for
equities: its own EMA200 status gates the other coins into a bearish regime
(max position size halved) like the equity system's bearish_ema regime --
BTC is "crypto's SPY", the benchmark the rest of the market takes its cue
from. Unlike equities, bearish-EMA does NOT also require 3/3 confidence here
(see crypto_signals.py's BEARISH_EMA_MIN_CONFIDENCE for why: BTC spends long
stretches below its own 200-EMA, so that extra tightening left the backtest
with zero trades).

Usage:
    python -m strategy.crypto_engine
    python -m strategy.crypto_engine --quick   # print only, no file save
"""

import json
import os
import sys
from datetime import datetime, timezone

from .market_data import fetch_ohlcv
from .indicators import compute_all
from .signals import generate_signal
from .circuit_breaker import check as check_kill_switch
from .crypto_signals import (
    CRYPTO_TICKERS, MAX_CRYPTO_ALLOCATION, MAX_POSITION_SIZE, MAX_POSITIONS,
    MIN_TRADE_SIZE, DATA_PERIOD, DATA_INTERVAL, ATR_VOLATILITY_THRESHOLD,
    BEARISH_EMA_MIN_CONFIDENCE,
)

try:
    from tabulate import tabulate
    _HAS_TABULATE = True
except ImportError:
    _HAS_TABULATE = False


def run_analysis() -> dict:
    timestamp = datetime.now(timezone.utc).isoformat()
    quick = "--quick" in sys.argv

    account_ok, account_halt_reason = check_kill_switch()

    print(f"\n{'='*60}")
    print(f"  Crypto Signal Engine  {timestamp[:16]} UTC")
    print(f"  System   : INDEPENDENT (daily bars, same account as equities)")
    print(f"  Tickers  : {CRYPTO_TICKERS}")
    print(f"{'='*60}\n")

    if not account_ok:
        print(f"  TRADING HALTED — {account_halt_reason}")
        print(f"  Signals below are for reference only. Do not open new positions.\n")

    signals = {}
    market_bearish_ema = False
    market_bearish = False

    try:
        btc_df = compute_all(fetch_ohlcv("BTC-USD", period=DATA_PERIOD, interval=DATA_INTERVAL))
        btc_close = float(btc_df["close"].iloc[-1])
        btc_ema200 = float(btc_df["ema200"].iloc[-1])
        market_bearish_ema = btc_close < btc_ema200
        # BTC is crypto's SPY -- exempt from the panic filter (market_bearish=False,
        # it can't panic-suppress itself), but still subject to the bearish-EMA
        # confidence/size gate, same treatment SPY gets for equities.
        btc_sig = generate_signal("BTC-USD", btc_df, market_bearish=False,
                                  market_bearish_ema=market_bearish_ema,
                                  atr_threshold=ATR_VOLATILITY_THRESHOLD,
                                  bearish_ema_min_confidence=BEARISH_EMA_MIN_CONFIDENCE)
        signals["BTC-USD"] = btc_sig
        market_bearish = btc_sig.rsi < 30
        regime_tag = "BEARISH (BTC below 200-EMA)" if market_bearish_ema else "BULLISH (BTC above 200-EMA)"
        print(f"  [REGIME] BTC ${btc_close:,.2f} vs EMA200 ${btc_ema200:,.2f} → {regime_tag}")
        if market_bearish:
            print(f"  [REGIME] BTC RSI={btc_sig.rsi:.1f} < 30 — BUY signals suppressed on alts")
    except Exception as exc:
        print(f"  [WARN] BTC-USD: {exc}")

    for ticker in CRYPTO_TICKERS:
        if ticker == "BTC-USD":
            continue
        try:
            df = compute_all(fetch_ohlcv(ticker, period=DATA_PERIOD, interval=DATA_INTERVAL))
            signals[ticker] = generate_signal(ticker, df, market_bearish=market_bearish,
                                              market_bearish_ema=market_bearish_ema,
                                              atr_threshold=ATR_VOLATILITY_THRESHOLD,
                                              bearish_ema_min_confidence=BEARISH_EMA_MIN_CONFIDENCE)
        except Exception as exc:
            print(f"  [WARN] {ticker}: {exc}")

    if _HAS_TABULATE:
        rows = [[s.ticker, s.action, f"${s.price:,.2f}", f"{s.rsi:.1f}",
                 s.ema_trend, s.bb_signal, f"{s.confidence}/3"]
                for s in signals.values()]
        print(tabulate(rows, headers=["Ticker", "Action", "Price", "RSI", "EMA", "BB", "Conf"],
                       tablefmt="rounded_outline"))

    actionable = [s for s in signals.values() if s.action == "BUY" and s.confidence >= 2]
    if not account_ok:
        actionable = []

    strong_amt = MAX_POSITION_SIZE
    moderate_amt = max(MIN_TRADE_SIZE, round(MAX_POSITION_SIZE * 0.5, 2))
    print(f"\n  Actionable (conf>=2): {len(actionable)}")
    for s in actionable:
        amt = strong_amt if s.confidence >= 3 else moderate_amt
        print(f"  → BUY {s.ticker} @ ${s.price:,.2f}  amount=${amt}  | {s.reason}")

    report = {
        "timestamp": timestamp,
        "trading_halted": not account_ok,
        "halt_reason": account_halt_reason or None,
        "market_regime": "bearish_ema" if market_bearish_ema else "normal",
        "tickers": CRYPTO_TICKERS,
        "signals": [
            {"ticker": s.ticker, "action": s.action, "price": s.price,
             "rsi": round(s.rsi, 2), "ema_trend": s.ema_trend, "bb_signal": s.bb_signal,
             "confidence": s.confidence, "atr_pct": round(s.atr_pct, 4), "reason": s.reason}
            for s in signals.values()
        ],
        "actionable": [
            {"ticker": s.ticker, "price": s.price, "confidence": s.confidence,
             "amount": strong_amt if s.confidence >= 3 else moderate_amt, "reason": s.reason}
            for s in actionable
        ],
        "rules": {
            "max_crypto_allocation": MAX_CRYPTO_ALLOCATION,
            "max_position_size": MAX_POSITION_SIZE,
            "max_positions": MAX_POSITIONS,
            "min_trade_size": MIN_TRADE_SIZE,
        },
    }

    if not quick:
        os.makedirs("docs", exist_ok=True)
        os.makedirs("logs", exist_ok=True)
        with open("docs/crypto_signals.json", "w") as f:
            json.dump(report, f, indent=2)
        with open("logs/crypto_signals.json", "w") as f:
            json.dump(report, f, indent=2)
        print("\n[OK] Saved → docs/crypto_signals.json  logs/crypto_signals.json")

    return report


if __name__ == "__main__":
    run_analysis()
