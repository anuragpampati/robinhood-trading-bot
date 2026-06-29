#!/usr/bin/env python3
"""
Walk-forward backtest — RSI+VWAP+EMA strategy on hourly bars.

Usage:
    python backtest.py          # last 30 days
    python backtest.py --days 7 # last 7 days

No look-ahead bias: indicators are causal (EWM adjust=False, VWAP uses
cumsum per day). Signal at bar i only sees data up to bar i.
"""

import sys
import numpy as np
import pandas as pd
from datetime import timedelta

from strategy.market_data import fetch_ohlcv
from strategy.indicators import compute_all
from strategy.signals import generate_signal
from strategy.config import (
    WATCHLIST, CASH_BUFFER, MAX_POSITION_SIZE, MIN_TRADE_SIZE,
    MAX_OPEN_POSITIONS, STOP_LOSS_PCT, TAKE_PROFIT_PCT, MARKET_REGIME_RSI_MIN,
)

TEST_DAYS = 30
for i, arg in enumerate(sys.argv):
    if arg == "--days" and i + 1 < len(sys.argv):
        TEST_DAYS = int(sys.argv[i + 1])

WARMUP_DAYS = 60   # extra history for indicator warmup (RSI needs ~14+ bars)
INITIAL_CASH = 100.0


def in_trade_window(ts: pd.Timestamp) -> bool:
    """10:00–15:30 ET only — avoids volatile open and close."""
    et = ts.tz_convert("America/New_York")
    if et.weekday() >= 5:
        return False
    return (10, 0) <= (et.hour, et.minute) <= (15, 30)


def run():
    fetch_period = f"{TEST_DAYS + WARMUP_DAYS}d"
    print(f"Fetching {fetch_period} of hourly data for {WATCHLIST}...")
    raw = {}
    for ticker in WATCHLIST:
        try:
            df = fetch_ohlcv(ticker, period=fetch_period, interval="1h")
            raw[ticker] = compute_all(df)
            print(f"  {ticker}: {len(df)} bars")
        except Exception as e:
            print(f"  [WARN] {ticker}: {e}")

    if "SPY" not in raw:
        sys.exit("ERROR: SPY required for regime filter")

    # Test window: last TEST_DAYS calendar days
    spine = raw["SPY"].index
    test_start = spine[-1] - timedelta(days=TEST_DAYS)
    test_bars = [ts for ts in spine if ts >= test_start and in_trade_window(ts)]
    print(f"\nBacktest: {test_bars[0].strftime('%Y-%m-%d')} → "
          f"{test_bars[-1].strftime('%Y-%m-%d')}  ({len(test_bars)} tradeable bars)\n")

    # ── Buy-and-hold SPY baseline ─────────────────────────────────────────────
    spy_prices = raw["SPY"]["close"]
    spy_start  = float(spy_prices.loc[:test_bars[0]].iloc[-1])
    spy_end    = float(spy_prices.loc[:test_bars[-1]].iloc[-1])
    bah_return = (spy_end - spy_start) / spy_start

    # ── Portfolio state ───────────────────────────────────────────────────────
    cash = INITIAL_CASH
    positions: dict[str, dict] = {}   # ticker → {qty, entry_price, cost, bars_held}
    trades: list[dict] = []

    peak_pv = INITIAL_CASH
    max_dd  = 0.0

    for bar_ts in test_bars:
        # current prices for all tickers (last close at or before this bar)
        prices = {}
        for tk in WATCHLIST:
            if tk in raw:
                slice_ = raw[tk].loc[:bar_ts]
                if not slice_.empty:
                    prices[tk] = float(slice_["close"].iloc[-1])

        # regime filter — SPY RSI at this bar
        spy_slice = raw["SPY"].loc[:bar_ts]
        spy_rsi = float(spy_slice["rsi"].iloc[-1]) if not spy_slice.empty else 50.0
        market_bearish = spy_rsi < MARKET_REGIME_RSI_MIN

        # ── SELL: stop-loss / take-profit / signal ────────────────────────────
        for tk in list(positions):
            if tk not in prices:
                continue
            pos   = positions[tk]
            price = prices[tk]
            entry = pos["entry_price"]

            if price <= entry * (1 - STOP_LOSS_PCT):
                reason = f"STOP_LOSS {price/entry-1:+.1%}"
            elif price >= entry * (1 + TAKE_PROFIT_PCT):
                reason = f"TAKE_PROFIT {price/entry-1:+.1%}"
            else:
                sig = generate_signal(tk, raw[tk].loc[:bar_ts], market_bearish=False)
                reason = f"SIGNAL SELL" if sig.action == "SELL" else None

            if reason:
                proceeds = pos["qty"] * price
                pnl      = proceeds - pos["cost"]
                cash    += proceeds
                trades.append(dict(
                    ts=bar_ts, ticker=tk, side="SELL", price=price,
                    pnl=pnl, reason=reason, bars=pos["bars_held"],
                ))
                del positions[tk]

        # ── BUY: signal-based ─────────────────────────────────────────────────
        for tk in WATCHLIST:
            if tk in positions or tk not in prices:
                continue
            if len(positions) >= MAX_OPEN_POSITIONS:
                break

            sig = generate_signal(tk, raw[tk].loc[:bar_ts], market_bearish=market_bearish)
            if sig.action != "BUY":
                continue

            amount = min(MAX_POSITION_SIZE, cash - CASH_BUFFER)
            if amount < MIN_TRADE_SIZE:
                continue

            price = prices[tk]
            qty   = amount / price
            cash -= amount
            positions[tk] = dict(
                qty=qty, entry_price=price, cost=amount, bars_held=0,
            )
            trades.append(dict(
                ts=bar_ts, ticker=tk, side="BUY", price=price,
                pnl=None, reason=sig.reason, bars=None,
            ))

        for pos in positions.values():
            pos["bars_held"] += 1

        pv      = cash + sum(positions[tk]["qty"] * prices.get(tk, positions[tk]["entry_price"])
                             for tk in positions)
        peak_pv = max(peak_pv, pv)
        max_dd  = max(max_dd, (peak_pv - pv) / peak_pv)

    # Mark open positions to market at last bar
    last_prices = {tk: float(raw[tk]["close"].iloc[-1]) for tk in WATCHLIST if tk in raw}
    final_value = cash + sum(
        pos["qty"] * last_prices.get(tk, pos["entry_price"])
        for tk, pos in positions.items()
    )
    for tk, pos in positions.items():
        price = last_prices.get(tk, pos["entry_price"])
        trades.append(dict(
            ts=test_bars[-1], ticker=tk, side="OPEN", price=price,
            pnl=pos["qty"] * price - pos["cost"],
            reason="still held", bars=pos["bars_held"],
        ))

    # ── Report ────────────────────────────────────────────────────────────────
    total_return = (final_value - INITIAL_CASH) / INITIAL_CASH
    closed = [t for t in trades if t["side"] == "SELL"]
    buys   = [t for t in trades if t["side"] == "BUY"]
    open_  = [t for t in trades if t["side"] == "OPEN"]
    wins   = [t for t in closed if t["pnl"] > 0]
    losses = [t for t in closed if t["pnl"] <= 0]
    win_rate = len(wins) / len(closed) if closed else 0

    print("=" * 62)
    print(f"  BACKTEST RESULTS  (last {TEST_DAYS} days, hourly bars)")
    print("=" * 62)
    print(f"  Strategy return   : {total_return:+.2%}  (${INITIAL_CASH:.0f} → ${final_value:.2f})")
    print(f"  Buy-and-hold SPY  : {bah_return:+.2%}")
    print(f"  Max drawdown      : {max_dd:.2%}")
    print(f"  Trades            : {len(buys)} buys → {len(closed)} closed, {len(open_)} still open")
    print(f"  Win rate          : {win_rate:.0%}  ({len(wins)}W / {len(losses)}L)")
    if wins:
        print(f"  Avg win P&L       : ${np.mean([t['pnl'] for t in wins]):.2f}")
    if losses:
        print(f"  Avg loss P&L      : ${np.mean([t['pnl'] for t in losses]):.2f}")
    if closed:
        rr = abs(np.mean([t['pnl'] for t in wins]) / np.mean([t['pnl'] for t in losses])) if wins and losses else 0
        print(f"  Actual R:R        : 1:{rr:.1f}")

    if closed or open_:
        print(f"\n  {'DATE':10}  {'TKR':4}  {'SIDE':5}  {'PRICE':>8}  {'P&L':>8}  {'BARS':>5}  REASON")
        print(f"  {'-'*10}  {'-'*4}  {'-'*5}  {'-'*8}  {'-'*8}  {'-'*5}  {'-'*30}")
        for t in trades:
            if t["side"] == "BUY":
                continue
            pnl_str  = f"${t['pnl']:+.2f}" if t["pnl"] is not None else "—"
            bars_str = str(t["bars"]) if t["bars"] is not None else "—"
            print(f"  {t['ts'].strftime('%Y-%m-%d'):10}  {t['ticker']:4}  {t['side']:5}  "
                  f"${t['price']:>7.2f}  {pnl_str:>8}  {bars_str:>5}  {t['reason'][:40]}")

    if buys:
        print(f"\n  BUY signals fired:")
        for t in buys:
            print(f"  {t['ts'].strftime('%Y-%m-%d %H:%M')}  {t['ticker']:4}  ${t['price']:.2f}  {t['reason'][:55]}")

    if not buys:
        print("\n  No buy signals fired in this period.")
        print("  (Check regime filter, RSI threshold, ATR gate in config.py)")


if __name__ == "__main__":
    run()
