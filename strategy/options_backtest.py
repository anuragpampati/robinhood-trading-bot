"""
Options strategy backtest — Black-Scholes simulation on DAILY bars.

Uses the same signal logic as strategy/options_engine.py (daily RSI + EMA50).
Completely independent of the equity backtest (backtest.py).

Usage:
    python -m strategy.options_backtest          # 90-day test, all tickers
    python -m strategy.options_backtest --days 30
    python -m strategy.options_backtest --ticker NVDA --days 60
"""

import math
import sys
from collections import Counter
from datetime import timedelta

import numpy as np
import pandas as pd
from scipy.stats import norm

from .market_data import fetch_ohlcv
from .options_signals import (
    OPTIONS_TICKERS, MAX_SPEND, TAKE_PROFIT_PCT, STOP_LOSS_PCT,
    MIN_DTE, TARGET_DTE, OTM_PCT,
)
from .options_engine import _rsi as _opt_rsi, _hv, RSI_CALL_MOD, RSI_PUT_MOD, RSI_CALL_STRONG, RSI_PUT_STRONG

# ── CLI args ──────────────────────────────────────────────────────────────────
TEST_DAYS     = 90
RISK_FREE     = 0.05   # annualised risk-free rate

for i, arg in enumerate(sys.argv):
    if arg == "--days" and i + 1 < len(sys.argv):
        TEST_DAYS = int(sys.argv[i + 1])

SINGLE_TICKER = None
for i, arg in enumerate(sys.argv):
    if arg == "--ticker" and i + 1 < len(sys.argv):
        SINGLE_TICKER = sys.argv[i + 1].upper()


# ── Black-Scholes ─────────────────────────────────────────────────────────────

def bs_price(S, K, T, r, sigma, opt_type="call"):
    if T <= 0 or sigma <= 0 or S <= 0 or K <= 0:
        return max(0.0, S - K) if opt_type == "call" else max(0.0, K - S)
    d1 = (math.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * math.sqrt(T))
    d2 = d1 - sigma * math.sqrt(T)
    if opt_type == "call":
        return S * norm.cdf(d1) - K * math.exp(-r * T) * norm.cdf(d2)
    return K * math.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)


def bs_delta(S, K, T, r, sigma, opt_type="call"):
    if T <= 0 or sigma <= 0:
        return 0.0
    d1 = (math.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * math.sqrt(T))
    return norm.cdf(d1) if opt_type == "call" else -norm.cdf(-d1)


# ── Core backtest ─────────────────────────────────────────────────────────────

def run_backtest_for(ticker: str, daily_df: pd.DataFrame) -> list[dict]:
    """
    Simulate the options strategy on one ticker using DAILY bars.
    Signal logic mirrors options_engine.py exactly.
    """
    trades    = []
    open_pos  = None

    close     = daily_df["close"].dropna()
    test_start = close.index[-1] - timedelta(days=TEST_DAYS)
    bars      = [ts for ts in close.index if ts >= test_start]

    for i, bar_ts in enumerate(bars):
        hist = close.loc[:bar_ts]
        if len(hist) < 55:    # need 50+ bars for EMA50
            continue
        price  = float(hist.iloc[-1])
        ema50  = float(hist.ewm(span=50, adjust=False).mean().iloc[-1])
        rsi    = float(_opt_rsi(hist, 14).iloc[-1])
        hv     = _hv(hist, min(20, len(hist) - 1))

        # ── Manage open position ─────────────────────────────────────────────
        if open_pos is not None:
            dte     = (open_pos["expiry"] - bar_ts.date()).days
            T       = max(dte / 365.0, 1 / 365.0)
            prem    = bs_price(price, open_pos["strike"], T, RISK_FREE, hv,
                               open_pos["opt_type"])
            pnl_pct = (prem - open_pos["entry_prem"]) / open_pos["entry_prem"]
            cost    = open_pos["entry_prem"] * 100

            reason = None
            if pnl_pct >= TAKE_PROFIT_PCT:
                reason = f"TAKE_PROFIT +{pnl_pct:.0%}"
            elif pnl_pct <= -STOP_LOSS_PCT:
                reason = f"STOP_LOSS {pnl_pct:.0%}"
            elif dte <= MIN_DTE:
                reason = f"FORCE_CLOSE DTE={dte}"

            if reason:
                proceeds = prem * 100
                trades.append({
                    "side":        "CLOSE",
                    "ticker":      ticker,
                    "opt_type":    open_pos["opt_type"],
                    "entry_ts":    open_pos["entry_ts"],
                    "exit_ts":     bar_ts,
                    "entry_px":    open_pos["entry_px"],
                    "exit_px":     price,
                    "strike":      open_pos["strike"],
                    "entry_prem":  open_pos["entry_prem"],
                    "exit_prem":   prem,
                    "entry_delta": open_pos["entry_delta"],
                    "cost":        cost,
                    "proceeds":    proceeds,
                    "pnl":         proceeds - cost,
                    "pnl_pct":     pnl_pct,
                    "reason":      reason,
                    "days_held":   (bar_ts.date() - open_pos["entry_ts"].date()).days,
                })
                open_pos = None
            continue   # don't open while managing an open position

        # ── Entry signal — same logic as options_engine.py ──────────────────
        # Pure RSI mean-reversion; no trend filter (see options_engine.py)
        if rsi < RSI_CALL_MOD:
            opt_type   = "call"
            action_str = "BUY_CALL"
        elif rsi > RSI_PUT_MOD:
            opt_type   = "put"
            action_str = "BUY_PUT"
        else:
            continue

        strike = round(price * (1 + OTM_PCT) if opt_type == "call"
                       else price * (1 - OTM_PCT), 0)
        T      = TARGET_DTE / 365.0
        prem   = bs_price(price, strike, T, RISK_FREE, hv, opt_type)
        delta  = bs_delta(price, strike, T, RISK_FREE, hv, opt_type)
        cost   = prem * 100

        if cost < 3 or cost > MAX_SPEND:
            continue   # outside budget

        expiry   = (bar_ts + timedelta(days=TARGET_DTE)).date()
        open_pos = {
            "entry_ts":   bar_ts,
            "entry_px":   price,
            "opt_type":   opt_type,
            "strike":     strike,
            "entry_prem": prem,
            "entry_delta": round(delta, 3),
            "expiry":     expiry,
        }

        trades.append({
            "side":        "OPEN",
            "ticker":      ticker,
            "opt_type":    opt_type,
            "action":      action_str,
            "entry_ts":    bar_ts,
            "entry_px":    price,
            "strike":      strike,
            "entry_prem":  prem,
            "entry_delta": round(delta, 3),
            "ema50":       round(ema50, 2),
            "rsi":         round(rsi, 2),
            "cost":        cost,
        })

    # Force-close anything still open at end of test window
    if open_pos is not None:
        price = float(close.iloc[-1])
        hv    = _hv(close, 20)
        dte   = max((open_pos["expiry"] - close.index[-1].date()).days, 0)
        T     = max(dte / 365.0, 1 / 365.0)
        prem  = bs_price(price, open_pos["strike"], T, RISK_FREE, hv, open_pos["opt_type"])
        cost  = open_pos["entry_prem"] * 100
        pnl_pct = (prem - open_pos["entry_prem"]) / open_pos["entry_prem"]
        trades.append({
            "side":       "CLOSE",
            "ticker":     ticker,
            "opt_type":   open_pos["opt_type"],
            "entry_ts":   open_pos["entry_ts"],
            "exit_ts":    close.index[-1],
            "entry_px":   open_pos["entry_px"],
            "exit_px":    price,
            "strike":     open_pos["strike"],
            "entry_prem": open_pos["entry_prem"],
            "exit_prem":  prem,
            "entry_delta": open_pos["entry_delta"],
            "cost":        cost,
            "proceeds":    prem * 100,
            "pnl":         prem * 100 - cost,
            "pnl_pct":     pnl_pct,
            "reason":      "END_OF_TEST",
            "days_held":   (close.index[-1].date() - open_pos["entry_ts"].date()).days,
        })

    return trades


# ── Main ──────────────────────────────────────────────────────────────────────

def run():
    universe     = [SINGLE_TICKER] if SINGLE_TICKER else OPTIONS_TICKERS
    fetch_period = f"{TEST_DAYS + 120}d"

    print(f"\n{'='*65}")
    print(f"  Options Strategy Backtest — Black-Scholes / DAILY bars")
    print(f"  Period  : last {TEST_DAYS} days | Tickers : {universe}")
    print(f"  Signal  : daily RSI + EMA50 (same as options_engine.py)")
    print(f"  Rules   : conf≥2 | DTE={TARGET_DTE} | TP=+{TAKE_PROFIT_PCT:.0%} | "
          f"SL=-{STOP_LOSS_PCT:.0%} | close≤{MIN_DTE}DTE")
    print(f"  Budget  : ≤${MAX_SPEND:.0f}/contract")
    print(f"{'='*65}\n")

    all_closes = []

    for ticker in universe:
        print(f"  {ticker}: fetching {fetch_period} daily data...", end=" ", flush=True)
        try:
            df = fetch_ohlcv(ticker, period=fetch_period, interval="1d")
            print(f"{len(df)} bars")
        except Exception as e:
            print(f"SKIP ({e})")
            continue

        tt     = run_backtest_for(ticker, df)
        opens  = [t for t in tt if t["side"] == "OPEN"]
        closes = [t for t in tt if t["side"] == "CLOSE"]

        if not opens:
            print(f"    → 0 signals in {TEST_DAYS}-day window")
            continue

        t_cost = sum(t["cost"] for t in closes)
        t_pnl  = sum(t["pnl"] for t in closes)
        wins   = [t for t in closes if t["pnl"] > 0]
        losses = [t for t in closes if t["pnl"] <= 0]
        wr     = len(wins) / len(closes) if closes else 0

        print(f"    → {len(opens)} trades  W:{len(wins)} L:{len(losses)}  "
              f"win={wr:.0%}  "
              f"net P&L ${t_pnl:+.2f} on ${t_cost:.2f} "
              f"({t_pnl/t_cost*100:+.1f}%)" if t_cost else "")

        for t in closes:
            print(f"       {t['entry_ts'].strftime('%Y-%m-%d'):10}  "
                  f"{t['opt_type']:4}  K${t['strike']:.0f}  "
                  f"Δ{t['entry_delta']:.2f}  "
                  f"RSI={t.get('rsi', '—')}  "
                  f"cost=${t['cost']:.2f}  "
                  f"pnl=${t['pnl']:+.2f} ({t['pnl_pct']:+.0%})  "
                  f"held {t['days_held']}d  {t['reason'][:28]}")

        # Inherit rsi/entry_delta from OPEN into CLOSE for display
        open_map = {t["entry_ts"]: t for t in opens}
        for t in closes:
            o = open_map.get(t["entry_ts"])
            if o:
                t.setdefault("rsi", o.get("rsi", "—"))
                t.setdefault("entry_delta", o.get("entry_delta", 0))

        all_closes.extend(closes)

    # ── Aggregate ─────────────────────────────────────────────────────────────
    print(f"\n{'─'*65}")
    print(f"  AGGREGATE — {TEST_DAYS}-day backtest, all tickers")
    print(f"{'─'*65}")

    if not all_closes:
        print("  No options trades fired.")
        print("  Reasons: RSI rarely hits <37 (call) or >63 (put) on large-caps in")
        print("  the test window, OR positions are expensive (>$75) in high-vol periods.")
        return

    t_cost = sum(t["cost"] for t in all_closes)
    t_pnl  = sum(t["pnl"] for t in all_closes)
    wins   = [t for t in all_closes if t["pnl"] > 0]
    losses = [t for t in all_closes if t["pnl"] <= 0]
    wr     = len(wins) / len(all_closes) if all_closes else 0
    avg_d  = np.mean([t.get("days_held", 0) for t in all_closes])
    avg_w  = np.mean([t["pnl"] for t in wins]) if wins else 0
    avg_l  = np.mean([t["pnl"] for t in losses]) if losses else 0

    print(f"  Total trades      : {len(all_closes)}")
    print(f"  Win rate          : {wr:.0%}  ({len(wins)}W / {len(losses)}L)")
    print(f"  Total premium out : ${t_cost:.2f}")
    print(f"  Total P&L         : ${t_pnl:+.2f}  ({t_pnl/t_cost*100:+.1f}% on premium)")
    print(f"  Avg win           : ${avg_w:+.2f}")
    print(f"  Avg loss          : ${avg_l:+.2f}")
    print(f"  Avg hold (days)   : {avg_d:.1f}")
    if wins and losses:
        print(f"  Actual R:R        : 1:{abs(avg_w/avg_l):.1f}")

    print(f"\n  Exit breakdown:")
    for tag, cnt in Counter(t["reason"].split(" ")[0] for t in all_closes).most_common():
        print(f"    {tag:20} {cnt}")

    over = [t for t in all_closes if t["cost"] > MAX_SPEND]
    print(f"\n  Budget: {len(all_closes)-len(over)}/{len(all_closes)} trades within ${MAX_SPEND:.0f}")


if __name__ == "__main__":
    run()
