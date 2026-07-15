"""
Options strategy backtest — Black-Scholes simulation.

Simulates buying long calls/puts based on the same RSI/EMA/BB signals used in
options_signals.py. Prices options via Black-Scholes using 30-day historical
vol as a proxy for IV. Tests the $75 max / 50% TP / 50% SL / force-close ≤5 DTE
rules over the last N days of hourly data.

Usage:
    python -m strategy.options_backtest          # 90-day test, default tickers
    python -m strategy.options_backtest --days 30
    python -m strategy.options_backtest --ticker NVDA --days 60
"""

import sys
import math
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from scipy.stats import norm

from .market_data import fetch_ohlcv
from .indicators import compute_all
from .signals import generate_signal
from .options_signals import (
    OPTIONS_TICKERS, MAX_SPEND, TAKE_PROFIT_PCT, STOP_LOSS_PCT,
    MIN_DTE_TO_HOLD, TARGET_DTE_MIN, TARGET_DTE_MAX
)

# ── CLI args ──────────────────────────────────────────────────────────────────
TEST_DAYS = 90
RISK_FREE = 0.05   # approximate 3-month T-bill rate

for i, arg in enumerate(sys.argv):
    if arg == "--days" and i + 1 < len(sys.argv):
        TEST_DAYS = int(sys.argv[i + 1])

SINGLE_TICKER = None
for i, arg in enumerate(sys.argv):
    if arg == "--ticker" and i + 1 < len(sys.argv):
        SINGLE_TICKER = sys.argv[i + 1].upper()


# ── Black-Scholes pricing ─────────────────────────────────────────────────────

def bs_price(S: float, K: float, T: float, r: float, sigma: float,
             opt_type: str = "call") -> float:
    """Black-Scholes option price. T in years, sigma annualised."""
    if T <= 0 or sigma <= 0:
        # intrinsic only
        if opt_type == "call":
            return max(0.0, S - K)
        return max(0.0, K - S)
    d1 = (math.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * math.sqrt(T))
    d2 = d1 - sigma * math.sqrt(T)
    if opt_type == "call":
        return S * norm.cdf(d1) - K * math.exp(-r * T) * norm.cdf(d2)
    return K * math.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)


def bs_delta(S: float, K: float, T: float, r: float, sigma: float,
             opt_type: str = "call") -> float:
    if T <= 0 or sigma <= 0:
        return 0.0
    d1 = (math.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * math.sqrt(T))
    return norm.cdf(d1) if opt_type == "call" else -norm.cdf(-d1)


def hist_vol(prices: pd.Series, window: int = 20) -> float:
    """Annualised historical vol from close prices (hourly → *sqrt(252*6.5))."""
    if len(prices) < window + 1:
        return 0.25  # fallback
    rets = np.log(prices / prices.shift(1)).dropna()
    # hourly vol → annualise by sqrt(252 trading days × 6.5 hours)
    return float(rets.tail(window).std() * math.sqrt(252 * 6.5))


def select_strike(S: float, opt_type: str, target_delta: float = 0.35) -> float:
    """Choose a strike ~5-8 % OTM that roughly corresponds to delta 0.35."""
    if opt_type == "call":
        return round(S * 1.055, 0)   # ~5.5 % OTM call
    return round(S * 0.945, 0)       # ~5.5 % OTM put


# ── Helpers ───────────────────────────────────────────────────────────────────

def in_trade_window(ts: pd.Timestamp) -> bool:
    et = ts.tz_convert("America/New_York")
    if et.weekday() >= 5:
        return False
    return (10, 0) <= (et.hour, et.minute) <= (15, 30)


def run_backtest_for(ticker: str, df: pd.DataFrame) -> list[dict]:
    """Run options backtest for a single ticker. Returns list of trade dicts."""
    trades = []
    open_pos: dict | None = None   # only one options position per ticker at a time

    spine = df.index
    test_start = spine[-1] - timedelta(days=TEST_DAYS)
    bars = [ts for ts in spine if ts >= test_start and in_trade_window(ts)]

    for bar_ts in bars:
        slice_df = df.loc[:bar_ts]
        price = float(slice_df["close"].iloc[-1])

        # ── Manage open position ─────────────────────────────────────────────
        if open_pos is not None:
            dte_remaining = (open_pos["expiry"] - bar_ts.date()).days
            hv = hist_vol(slice_df["close"])
            T = max(dte_remaining / 365.0, 1 / 365.0)
            current_premium = bs_price(price, open_pos["strike"], T,
                                       RISK_FREE, hv, open_pos["opt_type"])

            pnl_pct = (current_premium - open_pos["entry_premium"]) / open_pos["entry_premium"]
            cost = open_pos["contracts"] * open_pos["entry_premium"] * 100

            exit_reason = None
            if pnl_pct >= TAKE_PROFIT_PCT:
                exit_reason = f"TAKE_PROFIT +{pnl_pct:.0%}"
            elif pnl_pct <= -STOP_LOSS_PCT:
                exit_reason = f"STOP_LOSS {pnl_pct:.0%}"
            elif dte_remaining <= MIN_DTE_TO_HOLD:
                exit_reason = f"FORCE_CLOSE DTE={dte_remaining}"

            if exit_reason:
                proceeds = open_pos["contracts"] * current_premium * 100
                trades.append({
                    "ticker":      ticker,
                    "opt_type":    open_pos["opt_type"],
                    "side":        "CLOSE",
                    "entry_ts":    open_pos["entry_ts"],
                    "exit_ts":     bar_ts,
                    "entry_price": open_pos["entry_stock_price"],
                    "exit_price":  price,
                    "strike":      open_pos["strike"],
                    "entry_prem":  open_pos["entry_premium"],
                    "exit_prem":   current_premium,
                    "cost":        cost,
                    "proceeds":    proceeds,
                    "pnl":         proceeds - cost,
                    "pnl_pct":     pnl_pct,
                    "reason":      exit_reason,
                    "days_held":   (bar_ts.date() - open_pos["entry_ts"].date()).days,
                })
                open_pos = None
            continue   # don't open another while one is active

        # ── Check entry signal ───────────────────────────────────────────────
        try:
            sig = generate_signal(ticker, slice_df)
        except Exception:
            continue

        if sig.action == "HOLD" or sig.confidence < 2:
            continue
        opt_type = "call" if sig.action == "BUY" else "put"

        # Price the option at entry
        hv = hist_vol(slice_df["close"])
        entry_dte = 14
        T = entry_dte / 365.0
        strike = select_strike(price, opt_type)
        entry_premium = bs_price(price, strike, T, RISK_FREE, hv, opt_type)
        entry_delta = bs_delta(price, strike, T, RISK_FREE, hv, opt_type)

        # Skip if premium is 0 (deep OTM or bad vol) or over budget per contract
        cost_per_contract = entry_premium * 100
        if cost_per_contract < 5 or cost_per_contract > MAX_SPEND:
            continue

        contracts = 1
        expiry = (bar_ts + timedelta(days=entry_dte)).date()

        open_pos = {
            "entry_ts":         bar_ts,
            "entry_stock_price": price,
            "opt_type":         opt_type,
            "strike":           strike,
            "entry_premium":    entry_premium,
            "entry_delta":      entry_delta,
            "contracts":        contracts,
            "expiry":           expiry,
            "signal":           sig.action,
        }

        trades.append({
            "ticker":      ticker,
            "opt_type":    opt_type,
            "side":        "OPEN",
            "entry_ts":    bar_ts,
            "entry_price": price,
            "strike":      strike,
            "entry_prem":  entry_premium,
            "entry_delta": round(entry_delta, 3),
            "cost":        cost_per_contract,
            "reason":      sig.reason[:60],
        })

    # Force-close any still-open position at last bar
    if open_pos is not None:
        price = float(df["close"].iloc[-1])
        dte_remaining = max((open_pos["expiry"] - df.index[-1].date()).days, 0)
        hv = hist_vol(df["close"])
        T = max(dte_remaining / 365.0, 1 / 365.0)
        final_prem = bs_price(price, open_pos["strike"], T, RISK_FREE, hv, open_pos["opt_type"])
        cost = open_pos["contracts"] * open_pos["entry_premium"] * 100
        proceeds = open_pos["contracts"] * final_prem * 100
        pnl_pct = (final_prem - open_pos["entry_premium"]) / open_pos["entry_premium"]
        trades.append({
            "ticker":      ticker,
            "opt_type":    open_pos["opt_type"],
            "side":        "CLOSE",
            "entry_ts":    open_pos["entry_ts"],
            "exit_ts":     df.index[-1],
            "entry_price": open_pos["entry_stock_price"],
            "exit_price":  price,
            "strike":      open_pos["strike"],
            "entry_prem":  open_pos["entry_premium"],
            "exit_prem":   final_prem,
            "cost":        cost,
            "proceeds":    proceeds,
            "pnl":         proceeds - cost,
            "pnl_pct":     pnl_pct,
            "reason":      "END_OF_TEST",
            "days_held":   (df.index[-1].date() - open_pos["entry_ts"].date()).days,
        })

    return trades


# ── Main ──────────────────────────────────────────────────────────────────────

def run():
    universe = [SINGLE_TICKER] if SINGLE_TICKER else sorted(OPTIONS_TICKERS)
    fetch_period = f"{TEST_DAYS + 80}d"

    print(f"\n{'='*65}")
    print(f"  Options Strategy Backtest — Black-Scholes simulation")
    print(f"  Period : last {TEST_DAYS} days | Tickers : {universe}")
    print(f"  Rules  : entry conf≥2 | DTE=14 | TP=+50% | SL=-50% | close≤5DTE")
    print(f"  Budget : ≤${MAX_SPEND:.0f}/contract (1 contract max per ticker)")
    print(f"{'='*65}\n")

    all_closes: list[dict] = []
    skipped: list[str] = []

    for ticker in universe:
        print(f"  Fetching {fetch_period} hourly data for {ticker}...", end=" ", flush=True)
        try:
            df = compute_all(fetch_ohlcv(ticker, period=fetch_period, interval="1h"))
            print(f"{len(df)} bars")
        except Exception as e:
            print(f"SKIP ({e})")
            skipped.append(ticker)
            continue

        ticker_trades = run_backtest_for(ticker, df)
        closes = [t for t in ticker_trades if t["side"] == "CLOSE"]
        opens  = [t for t in ticker_trades if t["side"] == "OPEN"]

        if not opens:
            print(f"    → {ticker}: 0 signals fired in {TEST_DAYS}-day window")
            continue

        total_cost = sum(t["cost"] for t in closes)
        total_pnl  = sum(t["pnl"] for t in closes)
        wins = [t for t in closes if t["pnl"] > 0]
        losses = [t for t in closes if t["pnl"] <= 0]

        print(f"    → {ticker}: {len(opens)} trades | "
              f"W:{len(wins)} L:{len(losses)} | "
              f"net P&L ${total_pnl:+.2f} on ${total_cost:.2f} spent "
              f"({total_pnl/total_cost*100:+.1f}%)" if total_cost else "")

        for t in closes:
            print(f"       {t['entry_ts'].strftime('%Y-%m-%d'):10} "
                  f"{t['opt_type']:4} K${t['strike']:.0f} "
                  f"Δ{t.get('entry_delta', 0):.2f}  "
                  f"cost=${t['cost']:.2f}  "
                  f"pnl=${t['pnl']:+.2f} ({t['pnl_pct']:+.0%})  "
                  f"{t['reason'][:30]}")

        all_closes.extend(closes)

    # ── Aggregate results ─────────────────────────────────────────────────────
    print(f"\n{'─'*65}")
    print(f"  AGGREGATE RESULTS  ({TEST_DAYS}-day backtest, all tickers)")
    print(f"{'─'*65}")
    if not all_closes:
        print("  No options trades fired. Check signal thresholds or expand tickers.")
        print("\n  Diagnosis:")
        print("  • OPTIONS_TICKERS only fires on RSI conf≥2 for NVDA/AAPL/AMZN/META")
        print("  • Large-cap stable names rarely hit RSI<30 or >70 with confluence")
        print("  • Consider lowering confidence threshold or adding volatile names")
        return

    total_cost = sum(t["cost"] for t in all_closes)
    total_pnl  = sum(t["pnl"] for t in all_closes)
    wins = [t for t in all_closes if t["pnl"] > 0]
    losses = [t for t in all_closes if t["pnl"] <= 0]
    win_rate = len(wins) / len(all_closes) if all_closes else 0
    avg_win  = np.mean([t["pnl"] for t in wins]) if wins else 0
    avg_loss = np.mean([t["pnl"] for t in losses]) if losses else 0
    avg_days = np.mean([t.get("days_held", 0) for t in all_closes])

    print(f"  Total trades      : {len(all_closes)}")
    print(f"  Win rate          : {win_rate:.0%}  ({len(wins)}W / {len(losses)}L)")
    print(f"  Total premium out : ${total_cost:.2f}")
    print(f"  Total P&L         : ${total_pnl:+.2f}  ({total_pnl/total_cost*100:+.1f}% on premium)")
    print(f"  Avg win           : ${avg_win:+.2f}")
    print(f"  Avg loss          : ${avg_loss:+.2f}")
    print(f"  Avg hold (days)   : {avg_days:.1f}")
    if wins and losses:
        print(f"  Actual R:R        : 1:{abs(avg_win/avg_loss):.1f}")
    print(f"\n  Exit reasons:")
    from collections import Counter
    for reason, count in Counter(
        t["reason"].split(" ")[0] for t in all_closes
    ).most_common():
        print(f"    {reason:20} {count}")

    print(f"\n  Budget check (per trade):")
    over = [t for t in all_closes if t["cost"] > MAX_SPEND]
    print(f"    Trades within ${MAX_SPEND:.0f} budget : {len(all_closes)-len(over)}/{len(all_closes)}")
    if over:
        print(f"    Over budget (would be skipped)  : {len(over)}")


if __name__ == "__main__":
    run()
