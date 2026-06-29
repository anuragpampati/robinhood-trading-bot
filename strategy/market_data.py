"""Fetch OHLCV market data — yfinance (local) or Robinhood historicals cache (cloud)."""

import json
try:
    import yfinance as yf
except ImportError:
    yf = None
import pandas as pd
from datetime import datetime, timezone
from .config import DATA_PERIOD, DATA_INTERVAL, WATCHLIST


def fetch_ohlcv(ticker: str, period: str = DATA_PERIOD, interval: str = DATA_INTERVAL) -> pd.DataFrame:
    """Return OHLCV DataFrame for *ticker*. Raises on empty data."""
    df = yf.download(ticker, period=period, interval=interval,
                     auto_adjust=True, progress=False)
    if df.empty:
        raise ValueError(f"No data returned for {ticker}")
    df.index = pd.to_datetime(df.index, utc=True)
    df.columns = [c.lower() if isinstance(c, str) else c[0].lower() for c in df.columns]
    return df


def fetch_all_watchlist(watchlist: list[str] = WATCHLIST) -> dict[str, pd.DataFrame]:
    """Fetch OHLCV for every ticker in *watchlist*. Skips failures."""
    result = {}
    for ticker in watchlist:
        try:
            result[ticker] = fetch_ohlcv(ticker)
        except Exception as exc:
            print(f"[WARN] {ticker}: {exc}")
    return result


def rh_json_to_df(data_points: list[dict]) -> pd.DataFrame:
    """Convert Robinhood get_equity_historicals data_points to an OHLCV DataFrame.

    Expects each element to have: begins_at, open_price, high_price, low_price,
    close_price, volume (strings/numbers as returned by the MCP tool).
    """
    rows = [
        {
            "open":   float(dp["open_price"]),
            "high":   float(dp["high_price"]),
            "low":    float(dp["low_price"]),
            "close":  float(dp["close_price"]),
            "volume": float(dp.get("volume", 0) or 0),
        }
        for dp in data_points
        if float(dp.get("close_price", 0) or 0) > 0  # skip empty bars
    ]
    index = pd.to_datetime(
        [dp["begins_at"] for dp in data_points
         if float(dp.get("close_price", 0) or 0) > 0],
        utc=True,
    )
    df = pd.DataFrame(rows, index=index)
    return df.sort_index()


def fetch_all_from_cache(cache_path: str) -> dict[str, pd.DataFrame]:
    """Load pre-fetched Robinhood historicals from a JSON cache file.

    The file must be a dict mapping ticker → list[data_point], where each
    data_point is a Robinhood historicals object (begins_at, *_price, volume).
    """
    with open(cache_path) as f:
        cache = json.load(f)
    result = {}
    for ticker, data_points in cache.items():
        try:
            df = rh_json_to_df(data_points)
            if df.empty:
                print(f"[WARN] {ticker}: empty after conversion")
            else:
                result[ticker] = df
        except Exception as exc:
            print(f"[WARN] {ticker}: {exc}")
    return result


def is_market_open() -> bool:
    """True if NYSE is currently open (naive check, no holiday calendar)."""
    now = datetime.now(timezone.utc)
    # NYSE is UTC-5 (EST) or UTC-4 (EDT)
    from datetime import timedelta
    # Use UTC-4 (EDT) as approximation for May–Nov, UTC-5 otherwise
    month = now.month
    offset = -4 if 3 <= month <= 11 else -5
    local = now + timedelta(hours=offset)
    if local.weekday() >= 5:
        return False
    open_time = local.replace(hour=9, minute=30, second=0, microsecond=0)
    close_time = local.replace(hour=16, minute=0, second=0, microsecond=0)
    return open_time <= local <= close_time


