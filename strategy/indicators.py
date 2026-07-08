"""Technical indicators: RSI, Bollinger Bands, EMA, ATR, volume ratio."""

import pandas as pd
import numpy as np
from .config import RSI_PERIOD, EMA_FAST, EMA_SLOW, ATR_PERIOD

BB_PERIOD = 20    # SMA lookback for Bollinger Bands
BB_STD    = 2.0   # standard deviation multiplier
VOL_MA    = 20    # bars for volume moving average


def rsi(close: pd.Series, period: int = RSI_PERIOD) -> pd.Series:
    delta = close.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.ewm(com=period - 1, min_periods=period).mean()
    avg_loss = loss.ewm(com=period - 1, min_periods=period).mean()
    rs = avg_gain / avg_loss.replace(0, np.nan)
    return 100 - (100 / (1 + rs))


def ema(series: pd.Series, period: int) -> pd.Series:
    return series.ewm(span=period, adjust=False).mean()


def bollinger(close: pd.Series) -> tuple[pd.Series, pd.Series, pd.Series]:
    """Returns (bb_lower, bb_mid, bb_upper). bb_pct = (close-lower)/(upper-lower)."""
    mid   = close.rolling(BB_PERIOD).mean()
    std   = close.rolling(BB_PERIOD).std()
    upper = mid + BB_STD * std
    lower = mid - BB_STD * std
    return lower, mid, upper


def atr(df: pd.DataFrame, period: int = ATR_PERIOD) -> pd.Series:
    h, l, c = df["high"], df["low"], df["close"]
    prev_c = c.shift(1)
    tr = pd.concat([h - l, (h - prev_c).abs(), (l - prev_c).abs()], axis=1).max(axis=1)
    return tr.ewm(span=period, adjust=False).mean()


def compute_all(df: pd.DataFrame) -> pd.DataFrame:
    """Attach RSI, EMA, Bollinger Bands, ATR, volume ratio columns."""
    out = df.copy()
    out["rsi"]       = rsi(out["close"])
    out["ema_fast"]  = ema(out["close"], EMA_FAST)
    out["ema_slow"]  = ema(out["close"], EMA_SLOW)
    out["ema200"]    = ema(out["close"], 200)
    bb_lower, bb_mid, bb_upper = bollinger(out["close"])
    out["bb_lower"]  = bb_lower
    out["bb_mid"]    = bb_mid
    out["bb_upper"]  = bb_upper
    band_width       = (bb_upper - bb_lower).replace(0, np.nan)
    out["bb_pct"]    = (out["close"] - bb_lower) / band_width   # 0=lower, 0.5=mid, 1=upper
    vol_ma           = out["volume"].rolling(VOL_MA).mean()
    out["vol_ratio"] = out["volume"] / vol_ma.replace(0, np.nan)
    out["atr"]       = atr(out)
    out["atr_pct"]   = out["atr"] / out["close"]
    return out
