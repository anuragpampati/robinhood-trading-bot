"""
Standalone Options Signal Engine — completely independent of equity system.

Uses DAILY bars and its own indicator set. Never imports from the equity
strategy (signals.py, indicators.py, run.py). Can be run as a standalone
module by its own CCR on a separate schedule.

Signals:
  BUY_CALL  — price above 50-day EMA (uptrend) + daily RSI oversold (<37)
  BUY_PUT   — price below 50-day EMA (downtrend) + daily RSI overbought (>63)
  HOLD      — neither condition met

IV proxy: HV20 vs HV90 — when short-term vol < long-term vol, options are
relatively cheap; adds +1 to confidence when true.

Usage:
    python -m strategy.options_engine
    python -m strategy.options_engine --quick   # print only, no file save
"""

import json
import math
import os
import sys
from datetime import datetime, timezone

import numpy as np
import pandas as pd

try:
    from tabulate import tabulate
    _HAS_TABULATE = True
except ImportError:
    _HAS_TABULATE = False

from .market_data import fetch_ohlcv, is_market_open

# ── Tickers — liquid options with contracts affordable at ≤$75 each ───────────
# QQQ (~$515), MSFT (~$470): 5% OTM 14-DTE contracts cost $150-400 — excluded
OPTIONS_TICKERS = ["NVDA", "AAPL", "AMZN", "META"]

# ── Risk parameters (also read by CCR and backtest) ──────────────────────────
MAX_SPEND        = 75.0   # max premium per 1-contract purchase ($)
MAX_POSITIONS    = 2      # max concurrent positions across all tickers
TARGET_DTE       = 14     # target days-to-expiry when opening
OTM_PCT          = 0.055  # ~5.5% OTM for strike selection
TAKE_PROFIT_PCT  = 0.50   # close when premium gained +50%
STOP_LOSS_PCT    = 0.50   # close when premium lost -50%
MIN_DTE          = 5      # force-close at or below this DTE

# ── Signal thresholds (daily RSI, no trend filter) ───────────────────────────
# Trend filter (price vs EMA50) was removed: when RSI is oversold the stock
# is already in a short-term downtrend → EMA50 filter would never fire.
# Strategy: pure daily RSI mean-reversion for long calls/puts.
RSI_CALL_STRONG = 30   # extreme oversold → conf=3 (or +1 to base)
RSI_CALL_MOD    = 35   # moderate oversold → conf=2
RSI_PUT_STRONG  = 70   # extreme overbought → conf=3
RSI_PUT_MOD     = 65   # moderate overbought → conf=2


# ── Indicator helpers (self-contained, no equity dependency) ──────────────────

def _rsi(close: pd.Series, period: int = 14) -> pd.Series:
    delta = close.diff()
    gain  = delta.clip(lower=0).ewm(com=period - 1, adjust=False).mean()
    loss  = (-delta.clip(upper=0)).ewm(com=period - 1, adjust=False).mean()
    rs    = gain / loss.replace(0, np.nan)
    return 100 - 100 / (1 + rs)


def _hv(close: pd.Series, window: int) -> float:
    """Annualised historical vol from daily log-returns."""
    rets = np.log(close / close.shift(1)).dropna()
    return float(rets.tail(window).std() * math.sqrt(252)) if len(rets) >= window else 0.25


# ── Core signal function ──────────────────────────────────────────────────────

def analyse_ticker(ticker: str) -> dict:
    """Fetch daily bars, compute indicators, return options signal dict."""
    df    = fetch_ohlcv(ticker, period="120d", interval="1d")
    close = df["close"].dropna()   # drop partial/missing bars
    if close.empty:
        raise ValueError(f"No valid close data for {ticker}")
    price = float(close.iloc[-1])

    rsi   = float(_rsi(close, 14).iloc[-1])
    ema20 = float(close.ewm(span=20, adjust=False).mean().iloc[-1])
    ema50 = float(close.ewm(span=50, adjust=False).mean().iloc[-1])
    hv20  = _hv(close, 20)
    hv90  = _hv(close, 90)

    uptrend   = price > ema50     # informational only — not used as gate
    cheap_iv  = hv20 < hv90      # recent vol < long-term vol → options cheap

    action     = "HOLD"
    confidence = 0
    reason     = "no directional signal"

    # BUY_CALL: daily RSI oversold → expect mean-reversion bounce
    if rsi < RSI_CALL_MOD:
        action     = "BUY_CALL"
        confidence = 2
        reason     = f"RSI {rsi:.1f} oversold (daily) — mean-reversion call"
        if rsi < RSI_CALL_STRONG:
            confidence += 1
            reason     += " (extreme)"
        if cheap_iv:
            confidence  = min(confidence + 1, 4)
            reason     += " + cheap IV (HV20 < HV90)"

    # BUY_PUT: daily RSI overbought → expect mean-reversion pullback
    elif rsi > RSI_PUT_MOD:
        action     = "BUY_PUT"
        confidence = 2
        reason     = f"RSI {rsi:.1f} overbought (daily) — mean-reversion put"
        if rsi > RSI_PUT_STRONG:
            confidence += 1
            reason     += " (extreme)"
        if cheap_iv:
            confidence  = min(confidence + 1, 4)
            reason     += " + cheap IV (HV20 < HV90)"

    return {
        "ticker":     ticker,
        "action":     action,
        "confidence": confidence,
        "price":      round(price, 2),
        "rsi":        round(rsi, 2),
        "ema20":      round(ema20, 2),
        "ema50":      round(ema50, 2),
        "hv20":       round(hv20, 4),
        "hv90":       round(hv90, 4),
        "cheap_iv":   cheap_iv,
        "uptrend":    uptrend,     # informational — EMA50 used only for display
        "reason":     reason,
        # execution params for CCR
        "target_dte":      TARGET_DTE,
        "otm_pct":         OTM_PCT,
        "max_spend":       MAX_SPEND,
        "take_profit_pct": TAKE_PROFIT_PCT,
        "stop_loss_pct":   STOP_LOSS_PCT,
        "min_dte":         MIN_DTE,
    }


# ── Main ──────────────────────────────────────────────────────────────────────

def run_analysis() -> dict:
    market_open = is_market_open()
    timestamp   = datetime.now(timezone.utc).isoformat()
    quick       = "--quick" in sys.argv

    print(f"\n{'='*60}")
    print(f"  Options Signal Engine  {timestamp[:16]} UTC")
    print(f"  System   : INDEPENDENT (daily bars, not derived from equity)")
    print(f"  Tickers  : {OPTIONS_TICKERS}")
    print(f"  Market   : {'OPEN' if market_open else 'CLOSED'}")
    print(f"{'='*60}\n")

    signals = []
    for ticker in OPTIONS_TICKERS:
        try:
            print(f"  Analysing {ticker}...", end=" ", flush=True)
            sig = analyse_ticker(ticker)
            signals.append(sig)
            print(f"{sig['action']} (conf={sig['confidence']}) "
                  f"RSI={sig['rsi']:.1f}  "
                  f"{'↑ uptrend' if sig['uptrend'] else '↓ downtrend'}  "
                  f"IV {'cheap' if sig['cheap_iv'] else 'rich'}")
        except Exception as e:
            print(f"ERROR: {e}")

    print()
    actionable = [s for s in signals if s["action"] != "HOLD" and s["confidence"] >= 2]

    if _HAS_TABULATE:
        rows = [
            [s["ticker"],
             s["action"],
             f"{s['confidence']}/4",
             f"${s['price']:.2f}",
             f"{s['rsi']:.1f}",
             "↑ UP" if s["uptrend"] else "↓ DN",
             "CHEAP" if s["cheap_iv"] else "RICH",
             f"HV20={s['hv20']:.1%} HV90={s['hv90']:.1%}"]
            for s in signals
        ]
        print(tabulate(rows,
                       headers=["Ticker", "Signal", "Conf", "Price", "RSI",
                                 "Trend", "IV", "Vol"],
                       tablefmt="rounded_outline"))

    print(f"\n  Actionable (conf≥2): {len(actionable)}")
    for s in actionable:
        opt = "CALL" if s["action"] == "BUY_CALL" else "PUT"
        est_premium = s["price"] * OTM_PCT * 0.35  # rough delta * OTM dist
        print(f"  → {s['ticker']} {opt}  | "
              f"est. contract ~${est_premium*100:.0f}  | "
              f"{s['reason']}")

    if not market_open:
        print("\n  [INFO] Market closed — signals generated for reference only. "
              "No orders will be placed.")

    report = {
        "timestamp":     timestamp,
        "market_open":   market_open,
        "tickers":       OPTIONS_TICKERS,
        "signals":       signals,
        "actionable":    actionable,
        "max_positions": MAX_POSITIONS,
        "rules": {
            "max_spend_per_contract": MAX_SPEND,
            "target_dte":             TARGET_DTE,
            "otm_pct":                OTM_PCT,
            "take_profit_pct":        TAKE_PROFIT_PCT,
            "stop_loss_pct":          STOP_LOSS_PCT,
            "min_dte_to_hold":        MIN_DTE,
        },
    }

    if not quick:
        os.makedirs("docs", exist_ok=True)
        os.makedirs("logs", exist_ok=True)
        with open("docs/options_signals.json", "w") as f:
            json.dump(report, f, indent=2)
        with open("logs/options_signals.json", "w") as f:
            json.dump(report, f, indent=2)
        print("\n[OK] Saved → docs/options_signals.json  logs/options_signals.json")

    return report


if __name__ == "__main__":
    run_analysis()
