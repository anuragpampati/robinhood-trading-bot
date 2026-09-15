"""
Crypto system shared constants — imported by crypto_engine and crypto_backtest.
Mirrors strategy/options_signals.py's pattern: one file so both share the same
risk parameters without importing the full engine.

Crypto system is independent of equities and options -- same account, same
kill switch (real money, real drawdown), but its own signals, its own tracked
state (docs/crypto_positions.json), its own log (logs/crypto_trade_log.md).

Daily bars, not hourly -- equities on hourly bars turned out to whipsaw badly
(strategy/signals.py fix, 2026-09-13: 63% of exits were small trailing-stop
losses). Crypto is more volatile than equities intraday, so it would suffer
the same problem worse. Options already made this same choice for the same
reason; crypto follows it from the start instead of discovering it the hard way.
"""

# Liquid majors only, not the full Robinhood crypto catalog (91 pairs, most of
# them illiquid micro-cap tokens -- 33 of the 91 are halted in at least one
# region as of 2026-09). A $250 account with a $100 crypto sub-limit has no
# business in thin altcoins.
CRYPTO_TICKERS = ["BTC-USD", "ETH-USD", "SOL-USD", "XRP-USD", "LTC-USD",
                   "ADA-USD", "LINK-USD", "AVAX-USD", "DOGE-USD", "BCH-USD"]

MAX_CRYPTO_ALLOCATION = 100.0  # hard ceiling on total $ across all crypto positions
MAX_POSITION_SIZE     = 35.0   # max $ per individual coin
MAX_POSITIONS         = 3      # max concurrent crypto positions
# Equities' $15 floor left every weak (2/3 confidence) signal during bearish-EMA
# regime silently sized out: $35 * 0.5 (bearish) * 0.6 (low confidence) = $10.50
# < $15, so it never traded during ~85% of a recent 180d window. Crypto orders
# support much smaller increments than equities anyway (most pairs allow
# fractional-dollar orders well under $10).
MIN_TRADE_SIZE = 10.0

STOP_LOSS_PCT   = 0.08  # 8% below entry -- wider than equities' 5%, crypto is more volatile
TAKE_PROFIT_PCT = 0.15  # 15% above entry -- wider than equities' 10%, same reason

# Equities' ATR_VOLATILITY_THRESHOLD (3%, tuned for hourly bars) blocked nearly
# every crypto signal when first tested -- normal daily crypto ATR routinely
# runs 5-8%. 12% lets normal volatility through, still filters real chop.
ATR_VOLATILITY_THRESHOLD = 0.12

# Equities require 3/3 confidence when SPY is below its own 200-EMA (a rare
# regime flip for an index). BTC spent 154/181 days (85%) of a recent test
# window below its own 200-EMA -- a long recovery, not a rare flip. Requiring
# 3/3 through 85% of history left the backtest with zero trades. No extra
# tightening for crypto: same as the normal MIN_SIGNALS_TO_TRADE bar (2/3).
BEARISH_EMA_MIN_CONFIDENCE = 2

DATA_PERIOD   = "300d"  # matches options_engine's daily-bar warmup window
DATA_INTERVAL = "1d"
