"""Trading strategy configuration for a $100 Robinhood agentic account."""

# ── Capital & position sizing ─────────────────────────────────────────────────
TOTAL_CAPITAL = 100.0          # USD funded in agentic account
CASH_BUFFER = 10.0             # always keep this much uninvested
TRADEABLE_CAPITAL = TOTAL_CAPITAL - CASH_BUFFER  # $90

MAX_POSITION_SIZE = 20.0       # max dollars per position
MIN_TRADE_SIZE = 5.0           # don't place orders smaller than this
MAX_OPEN_POSITIONS = 4         # max concurrent holdings

# ── Watchlist ─────────────────────────────────────────────────────────────────
# Liquid, fractional-share eligible; blend of ETFs + blue-chips
WATCHLIST = ["SPY", "QQQ", "AAPL", "MSFT", "NVDA"]

# ── RSI parameters ───────────────────────────────────────────────────────────
RSI_PERIOD = 14
RSI_OVERSOLD = 35              # buy signal threshold — large caps bounce at 35, rarely hit 30
RSI_OVERBOUGHT = 70            # sell signal threshold (let winners run past 65)

# ── EMA parameters ───────────────────────────────────────────────────────────
EMA_FAST = 9
EMA_SLOW = 21

# ── ATR parameters ───────────────────────────────────────────────────────────
ATR_PERIOD = 14
ATR_VOLATILITY_THRESHOLD = 0.03  # skip trade if ATR/price > 3% (too volatile)

# ── Risk management ───────────────────────────────────────────────────────────
STOP_LOSS_PCT = 0.05           # 5% below entry → exit
TAKE_PROFIT_PCT = 0.10         # 10% above entry → exit
MIN_SIGNALS_TO_TRADE = 2       # need at least 2/3 indicators aligned

# ── Market data ───────────────────────────────────────────────────────────────
DATA_PERIOD = "60d"            # lookback window for indicator warmup
DATA_INTERVAL = "1h"           # 1-hour bars
VOLUME_LOOKBACK = 20           # days for avg-volume filter

# ── Market regime filter ──────────────────────────────────────────────────────
# Suppress buys during true market panic only — RSI 30-40 is normal correction territory
MARKET_REGIME_RSI_MIN = 30

# ── ATR trailing stop ─────────────────────────────────────────────────────────
ATR_STOP_MULTIPLIER = 2.0   # initial stop = entry − ATR_STOP_MULTIPLIER × ATR
TRAIL_LOCK1_PROFIT  = 0.025 # when profit ≥ +2.5 %, ratchet stop to entry + 0.5 %
TRAIL_LOCK1_STOP    = 0.005
TRAIL_LOCK2_PROFIT  = 0.050 # when profit ≥ +5.0 %, ratchet stop to entry + 2.5 %
TRAIL_LOCK2_STOP    = 0.025

# ── Market hours (ET) ─────────────────────────────────────────────────────────
MARKET_OPEN_HOUR = 9
MARKET_OPEN_MINUTE = 30
MARKET_CLOSE_HOUR = 16
AVOID_FIRST_MINUTES = 30       # skip first 30 min (volatile open)
AVOID_LAST_MINUTES = 30        # skip last 30 min (volatile close)
