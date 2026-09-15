#!/usr/bin/env python3
"""
Walk-forward backtest for the crypto system — daily bars, same mechanics as
backtest.py (equities) adapted for: BTC as regime anchor instead of SPY, no
market-hours window (crypto trades 24/7), crypto capital rules.

Usage:
    python -m strategy.crypto_backtest          # last 90 days
    python -m strategy.crypto_backtest --days 30
"""

import sys
import numpy as np
import pandas as pd
from datetime import timedelta

from strategy.market_data import fetch_ohlcv
from strategy.indicators import compute_all
from strategy.signals import generate_signal
from strategy.crypto_signals import (
    CRYPTO_TICKERS, MAX_CRYPTO_ALLOCATION, MAX_POSITION_SIZE, MAX_POSITIONS,
    MIN_TRADE_SIZE, STOP_LOSS_PCT, TAKE_PROFIT_PCT, DATA_PERIOD, DATA_INTERVAL,
    ATR_VOLATILITY_THRESHOLD, BEARISH_EMA_MIN_CONFIDENCE,
)
from strategy.config import (
    ATR_STOP_MULTIPLIER, TRAIL_LOCK1_PROFIT, TRAIL_LOCK1_STOP,
    TRAIL_LOCK2_PROFIT, TRAIL_LOCK2_STOP, MIN_HOLD_BARS,
    DAILY_LOSS_HALT, WEEKLY_LOSS_HALT,
)

TEST_DAYS = 90
EXPORT_RL = "--export-rl" in sys.argv
for i, arg in enumerate(sys.argv):
    if arg == "--days" and i + 1 < len(sys.argv):
        TEST_DAYS = int(sys.argv[i + 1])

WARMUP_DAYS = 210  # 200-bar EMA warmup + margin, daily bars
INITIAL_CASH = MAX_CRYPTO_ALLOCATION


def run():
    fetch_days = TEST_DAYS + WARMUP_DAYS
    print(f"Fetching {fetch_days}d of daily data for {CRYPTO_TICKERS}...")
    raw = {}
    for ticker in CRYPTO_TICKERS:
        try:
            df = fetch_ohlcv(ticker, period=f"{fetch_days}d", interval=DATA_INTERVAL)
            raw[ticker] = compute_all(df)
            print(f"  {ticker}: {len(df)} bars")
        except Exception as e:
            print(f"  [WARN] {ticker}: {e}")

    if "BTC-USD" not in raw:
        sys.exit("ERROR: BTC-USD required for regime filter")

    spine = raw["BTC-USD"].index
    test_start = spine[-1] - timedelta(days=TEST_DAYS)
    test_bars = [ts for ts in spine if ts >= test_start]
    print(f"\nBacktest: {test_bars[0].strftime('%Y-%m-%d')} → "
          f"{test_bars[-1].strftime('%Y-%m-%d')}  ({len(test_bars)} daily bars)\n")

    btc_prices = raw["BTC-USD"]["close"]
    btc_start  = float(btc_prices.loc[:test_bars[0]].iloc[-1])
    btc_end    = float(btc_prices.loc[:test_bars[-1]].iloc[-1])
    bah_return = (btc_end - btc_start) / btc_start

    cash = INITIAL_CASH
    positions: dict[str, dict] = {}
    trades: list[dict] = []
    peak_pv = INITIAL_CASH
    max_dd = 0.0
    day_open_pv, week_open_pv = {}, {}
    cb_halts = 0

    for bar_ts in test_bars:
        prices = {}
        for tk in CRYPTO_TICKERS:
            if tk in raw:
                slice_ = raw[tk].loc[:bar_ts]
                if not slice_.empty:
                    prices[tk] = float(slice_["close"].iloc[-1])

        btc_slice = raw["BTC-USD"].loc[:bar_ts]
        btc_rsi = float(btc_slice["rsi"].iloc[-1]) if not btc_slice.empty else 50.0
        market_bearish = btc_rsi < 30
        btc_close_now = float(btc_slice["close"].iloc[-1]) if not btc_slice.empty else 0.0
        btc_ema200_now = float(btc_slice["ema200"].iloc[-1]) if not btc_slice.empty else btc_close_now
        market_bearish_ema = btc_close_now < btc_ema200_now

        # SELL
        for tk in list(positions):
            if tk not in prices:
                continue
            pos, price, entry = positions[tk], prices[tk], positions[tk]["entry_price"]
            profit_pct = (price - entry) / entry
            trail = pos["trail_stop"]
            if profit_pct >= TRAIL_LOCK2_PROFIT:
                trail = max(trail, entry * (1 + TRAIL_LOCK2_STOP))
            elif profit_pct >= TRAIL_LOCK1_PROFIT:
                trail = max(trail, entry * (1 + TRAIL_LOCK1_STOP))
            pos["trail_stop"] = trail

            if price <= trail and pos["bars_held"] >= MIN_HOLD_BARS:
                reason = f"TRAIL_STOP {price/entry-1:+.1%} (stop=${trail:.4f})"
            elif price >= entry * (1 + TAKE_PROFIT_PCT):
                reason = f"TAKE_PROFIT {price/entry-1:+.1%}"
            else:
                sig = generate_signal(tk, raw[tk].loc[:bar_ts], atr_threshold=ATR_VOLATILITY_THRESHOLD,
                                      bearish_ema_min_confidence=BEARISH_EMA_MIN_CONFIDENCE)
                reason = "SIGNAL SELL" if sig.action == "SELL" else None

            if reason:
                proceeds = pos["qty"] * price
                pnl = proceeds - pos["cost"]
                cash += proceeds
                trades.append(dict(ts=bar_ts, ticker=tk, side="SELL", price=price,
                                    pnl=pnl, reason=reason, bars=pos["bars_held"]))
                del positions[tk]

        pv_now = cash + sum(positions[tk]["qty"] * prices.get(tk, positions[tk]["entry_price"])
                            for tk in positions)
        day_key, week_key = bar_ts.strftime("%Y-%m-%d"), bar_ts.strftime("%Y-W%W")
        day_open_pv.setdefault(day_key, pv_now)
        week_open_pv.setdefault(week_key, pv_now)
        daily_dd = (day_open_pv[day_key] - pv_now) / day_open_pv[day_key]
        weekly_dd = (week_open_pv[week_key] - pv_now) / week_open_pv[week_key]
        circuit_breaker_active = daily_dd >= DAILY_LOSS_HALT or weekly_dd >= WEEKLY_LOSS_HALT
        if circuit_breaker_active:
            cb_halts += 1

        # BUY
        if not circuit_breaker_active:
            for tk in CRYPTO_TICKERS:
                if tk in positions or tk not in prices:
                    continue
                if len(positions) >= MAX_POSITIONS:
                    break

                # BTC is crypto's SPY -- exempt from the PANIC filter only (mirrors
                # signals.py's `ticker != "SPY"` exemption, which only recognizes
                # "SPY" by name, not "BTC-USD" -- so this has to be handled by the
                # caller here). Still subject to the bearish-EMA confidence/size
                # gate below, same as SPY is for equities.
                sig = generate_signal(tk, raw[tk].loc[:bar_ts],
                                      market_bearish=(False if tk == "BTC-USD" else market_bearish),
                                      market_bearish_ema=market_bearish_ema,
                                      atr_threshold=ATR_VOLATILITY_THRESHOLD,
                                      bearish_ema_min_confidence=BEARISH_EMA_MIN_CONFIDENCE)
                if sig.action != "BUY":
                    continue

                pos_max = MAX_POSITION_SIZE * (0.5 if market_bearish_ema else 1.0)
                if sig.confidence < 3:
                    pos_max *= 0.6
                crypto_deployed = sum(p["cost"] for p in positions.values())
                room = MAX_CRYPTO_ALLOCATION - crypto_deployed
                amount = min(pos_max, cash, room)
                if amount < MIN_TRADE_SIZE:
                    continue

                price = prices[tk]
                qty = amount / price
                atr_stop = price * (1 - ATR_STOP_MULTIPLIER * sig.atr_pct) if sig.atr_pct > 0 else price * (1 - STOP_LOSS_PCT)
                cash -= amount
                positions[tk] = dict(qty=qty, entry_price=price, cost=amount, bars_held=0,
                                     trail_stop=atr_stop, atr_pct=sig.atr_pct)
                trades.append(dict(ts=bar_ts, ticker=tk, side="BUY", price=price,
                                    pnl=None, reason=sig.reason, bars=None, amount=amount))

        for pos in positions.values():
            pos["bars_held"] += 1

        pv = cash + sum(positions[tk]["qty"] * prices.get(tk, positions[tk]["entry_price"])
                        for tk in positions)
        peak_pv = max(peak_pv, pv)
        max_dd = max(max_dd, (peak_pv - pv) / peak_pv)

    last_prices = {tk: float(raw[tk]["close"].iloc[-1]) for tk in CRYPTO_TICKERS if tk in raw}
    final_value = cash + sum(pos["qty"] * last_prices.get(tk, pos["entry_price"])
                             for tk, pos in positions.items())
    for tk, pos in positions.items():
        price = last_prices.get(tk, pos["entry_price"])
        trades.append(dict(ts=test_bars[-1], ticker=tk, side="OPEN", price=price,
                            pnl=pos["qty"] * price - pos["cost"], reason="still held",
                            bars=pos["bars_held"]))

    total_return = (final_value - INITIAL_CASH) / INITIAL_CASH
    closed = [t for t in trades if t["side"] == "SELL"]
    buys = [t for t in trades if t["side"] == "BUY"]
    open_ = [t for t in trades if t["side"] == "OPEN"]
    wins = [t for t in closed if t["pnl"] > 0]
    losses = [t for t in closed if t["pnl"] <= 0]
    win_rate = len(wins) / len(closed) if closed else 0

    print("=" * 62)
    print(f"  CRYPTO BACKTEST RESULTS  (last {TEST_DAYS} days, daily bars)")
    print("=" * 62)
    print(f"  Strategy return   : {total_return:+.2%}  (${INITIAL_CASH:.0f} → ${final_value:.2f})")
    print(f"  Buy-and-hold BTC  : {bah_return:+.2%}")
    print(f"  Max drawdown      : {max_dd:.2%}")
    print(f"  Circuit breaker   : {cb_halts} bars halted ({DAILY_LOSS_HALT:.0%} daily / {WEEKLY_LOSS_HALT:.0%} weekly limits)")
    print(f"  Trades            : {len(buys)} buys -> {len(closed)} closed, {len(open_)} still open")
    print(f"  Win rate          : {win_rate:.0%}  ({len(wins)}W / {len(losses)}L)")
    if wins:
        print(f"  Avg win P&L       : ${np.mean([t['pnl'] for t in wins]):.2f}")
    if losses:
        print(f"  Avg loss P&L      : ${np.mean([t['pnl'] for t in losses]):.2f}")
    if closed and wins and losses:
        rr = abs(np.mean([t['pnl'] for t in wins]) / np.mean([t['pnl'] for t in losses]))
        print(f"  Actual R:R        : 1:{rr:.1f}")

    if closed or open_:
        print(f"\n  {'DATE':10}  {'TKR':9}  {'SIDE':5}  {'PRICE':>10}  {'P&L':>8}  {'BARS':>5}  REASON")
        for t in trades:
            if t["side"] == "BUY":
                continue
            pnl_str = f"${t['pnl']:+.2f}" if t["pnl"] is not None else "—"
            print(f"  {t['ts'].strftime('%Y-%m-%d'):10}  {t['ticker']:9}  {t['side']:5}  "
                  f"${t['price']:>9.4f}  {pnl_str:>8}  {str(t['bars']):>5}  {t['reason'][:40]}")

    if not buys:
        print("\n  No buy signals fired in this period.")


if __name__ == "__main__":
    run()
