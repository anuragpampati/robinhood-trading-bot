"""Generate BUY / SELL / HOLD signals from indicator data."""

from dataclasses import dataclass
import pandas as pd
from .config import (
    RSI_OVERSOLD, RSI_OVERBOUGHT,
    ATR_VOLATILITY_THRESHOLD, MIN_SIGNALS_TO_TRADE,
    MARKET_REGIME_RSI_MIN,
)

VOL_GATE = 0.7   # skip signal if volume < 70% of 20-bar average (thin/noise bar)


@dataclass
class Signal:
    ticker: str
    action: str          # "BUY" | "SELL" | "HOLD"
    price: float
    rsi: float
    ema_trend: str       # "BULLISH" | "BEARISH" | "NEUTRAL"
    bb_signal: str       # "BELOW_BAND" | "IN_BAND" | "ABOVE_BAND"
    confidence: int      # 0-3 (number of aligned indicators)
    atr_pct: float
    reason: str


def _ema_trend(row: pd.Series) -> str:
    if row["ema_fast"] > row["ema_slow"] * 1.001:
        return "BULLISH"
    if row["ema_fast"] < row["ema_slow"] * 0.999:
        return "BEARISH"
    return "NEUTRAL"


def _bb_position(row: pd.Series) -> str:
    """Where price sits in the Bollinger Band. BELOW_BAND = oversold zone."""
    pct = row.get("bb_pct", 0.5)
    if pd.isna(pct):
        return "IN_BAND"
    if pct < 0.2:
        return "BELOW_BAND"
    if pct > 0.8:
        return "ABOVE_BAND"
    return "IN_BAND"


def generate_signal(ticker: str, df: pd.DataFrame, market_bearish: bool = False) -> Signal:
    """Produce a trading signal for *ticker* from its indicator DataFrame.

    Three signals scored 0-3: RSI oversold/overbought, Bollinger Band position,
    EMA trend. Need MIN_SIGNALS_TO_TRADE (2) aligned for BUY or SELL.

    market_bearish: True when SPY RSI < MARKET_REGIME_RSI_MIN (market panic).
    SPY itself is exempt from market_bearish — it IS the market.

    Bollinger Bands replace VWAP: BB resets never (VWAP resets daily), making
    it far more meaningful for multi-day swing trades (Stefan Jansen, ch. 4).
    """
    df_clean = df.dropna(subset=["rsi", "ema_fast", "ema_slow", "bb_pct", "atr"])
    if df_clean.empty:
        return Signal(ticker, "HOLD", 0, 50, "NEUTRAL", "IN_BAND", 0, 0, "insufficient data")

    row     = df_clean.iloc[-1]
    price   = float(row["close"])
    rsi_val = float(row["rsi"])
    atr_pct = float(row["atr_pct"])
    trend   = _ema_trend(row)
    bb_pos  = _bb_position(row)

    # Volume gate — low-volume bars are noise, not signal
    vol_ratio = float(row.get("vol_ratio", 1.0) or 1.0)
    if vol_ratio < VOL_GATE and not pd.isna(row.get("vol_ratio")):
        return Signal(ticker, "HOLD", price, rsi_val, trend, bb_pos, 0, atr_pct,
                      f"low volume ({vol_ratio:.2f}x avg) — skipping")

    # Volatility gate — skip if market is too choppy
    if atr_pct > ATR_VOLATILITY_THRESHOLD:
        return Signal(ticker, "HOLD", price, rsi_val, trend, bb_pos, 0, atr_pct,
                      f"ATR too high ({atr_pct:.1%}) — skipping")

    # RSI slope — falling-knife guard (only counts as oversold if stabilizing)
    rsi_prev      = float(df_clean["rsi"].iloc[-4]) if len(df_clean) >= 4 else rsi_val
    rsi_still_falling = rsi_val < rsi_prev - 2.0

    # ── BUY scoring ──────────────────────────────────────────────────────────
    buy_score   = 0
    buy_reasons = []

    if rsi_val < RSI_OVERSOLD:
        if rsi_still_falling:
            buy_reasons.append(f"RSI oversold ({rsi_val:.1f}) but still falling — wait")
        else:
            buy_score += 1
            direction = "↑" if rsi_val >= rsi_prev else "≈"
            buy_reasons.append(f"RSI oversold+stabilizing ({rsi_prev:.1f}{direction}{rsi_val:.1f})")

    if bb_pos == "BELOW_BAND" and len(df_clean) >= 2:
        prev_bb = float(df_clean["bb_pct"].iloc[-2])
        curr_bb = float(row["bb_pct"])
        if curr_bb > prev_bb:
            # price recovering within below-band territory (reversal in progress)
            buy_score += 1
            buy_reasons.append(f"BB reversal: {prev_bb:.2f}→{curr_bb:.2f} (returning from band)")
        # if still falling below band → don't count (walking the lower band in downtrend)

    if trend == "BULLISH":
        buy_score += 1
        buy_reasons.append("EMA bullish crossover")

    # ── SELL scoring ─────────────────────────────────────────────────────────
    # RSI overbought REQUIRED for sell — BB/EMA alone can signal mid-bounce.
    rsi_overbought = rsi_val > RSI_OVERBOUGHT
    sell_score     = 0
    sell_reasons   = []

    if rsi_overbought:
        sell_score += 1
        sell_reasons.append(f"RSI overbought ({rsi_val:.1f})")
    if bb_pos == "ABOVE_BAND":
        sell_score += 1
        sell_reasons.append("price above BB upper band")
    if trend == "BEARISH":
        sell_score += 1
        sell_reasons.append("EMA bearish")

    # BUY: suppress individual tickers during market panic (not corrections)
    # SPY is exempt — it IS the market
    if buy_score >= MIN_SIGNALS_TO_TRADE and buy_score > sell_score:
        if market_bearish and ticker != "SPY":
            return Signal(ticker, "HOLD", price, rsi_val, trend, bb_pos, buy_score, atr_pct,
                          f"BUY suppressed — SPY RSI < {MARKET_REGIME_RSI_MIN} (market panic)")
        return Signal(ticker, "BUY", price, rsi_val, trend, bb_pos,
                      buy_score, atr_pct, " | ".join(buy_reasons))

    # SELL: RSI overbought must be present
    if rsi_overbought and sell_score >= MIN_SIGNALS_TO_TRADE and sell_score > buy_score:
        return Signal(ticker, "SELL", price, rsi_val, trend, bb_pos,
                      sell_score, atr_pct, " | ".join(sell_reasons))

    reason = f"RSI={rsi_val:.1f} ({'falling' if rsi_still_falling else 'stable'}), BB={bb_pos}, EMA={trend}"
    return Signal(ticker, "HOLD", price, rsi_val, trend, bb_pos, 0, atr_pct, reason)
