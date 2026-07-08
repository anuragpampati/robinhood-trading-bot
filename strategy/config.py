"""Trading strategy configuration for a $100 Robinhood agentic account."""

# ── Capital & position sizing ─────────────────────────────────────────────────
TOTAL_CAPITAL = 100.0          # USD funded in agentic account
CASH_BUFFER = 10.0             # always keep this much uninvested
TRADEABLE_CAPITAL = TOTAL_CAPITAL - CASH_BUFFER  # $90

MAX_POSITION_SIZE = 20.0       # max dollars per position
MIN_TRADE_SIZE = 5.0           # don't place orders smaller than this
MAX_OPEN_POSITIONS = 4         # max concurrent holdings

# ── Watchlist ─────────────────────────────────────────────────────────────────
# 103 tickers: core + sector themes (Space, Quantum, Drones, Nuclear, Photonics,
# CPU, Physical AI, AI Utilities, AI Power, AI Connectivity, AI Hardware, AI Applications)
WATCHLIST = [
    # Market ETFs
    "SPY", "QQQ", "IWM",
    # Mega-cap tech
    "AAPL", "MSFT", "NVDA", "AMD", "INTC", "QCOM", "AVGO", "MU", "CRM",
    # Big tech / growth
    "AMZN", "GOOGL", "META", "TSLA", "NFLX", "UBER", "COIN", "SNAP",
    # Robinhood-popular
    "PLTR", "SOFI", "HOOD", "RIVN", "ARM",
    # Finance
    "JPM", "BAC", "GS", "C", "WFC",
    # Healthcare
    "JNJ", "PFE", "MRNA",
    # Consumer
    "DIS", "SBUX", "MCD", "WMT", "TGT",
    # Industrial / Auto
    "BA", "GE", "F", "GM",
    # Energy
    "XOM", "CVX",
    # Fintech / payments
    "PYPL", "SQ",
    # High-growth
    "SHOP", "RBLX", "DKNG", "ORCL",
    # AI & data companies
    "SNOW", "AI", "SOUN",
    # AI data center infrastructure
    "SMCI", "VRT", "DELL", "EQIX",
    # Semiconductor equipment & advanced chips
    "AMAT", "LRCX", "KLAC", "MRVL", "TXN", "ASML",
    # Space
    "RKLB", "ASTS", "PL", "RDW",
    # Physical AI — robotics, autonomous driving, industrial automation
    "ISRG", "SYM", "MBLY", "TER", "ROK", "AUR", "LAZR",
    # Quantum computing
    "IONQ", "RGTI", "QBTS", "INFQ",
    # Drones & defense
    "ONDS", "AVAV", "KTOS", "MRCY",
    # Nuclear energy
    "OKLO", "UUUU", "GEV", "LEU",
    # Photonics
    "AAOI", "LITE", "COHR", "AEHR",
    # CPU / advanced packaging
    "AMKR", "TSM",
    # AI Utilities (compute/mining)
    "IREN", "NBIS", "CIFR", "CRWV",
    # AI Power
    "EOSE", "BE", "NVTS",
    # AI Connectivity
    "ALAB", "CRDO",
    # AI Applications
    "NOW", "CRWD",
]

# ── Fibonacci target levels (upside Fibonacci levels by ticker) ───────────────
# Reference price targets for dashboard display. NOT used for automated exits.
FIB_TARGETS: dict[str, float] = {
    # Space
    "RKLB": 92, "ASTS": 79, "PL": 26, "RDW": 8,
    # Quantum
    "IONQ": 44, "RGTI": 16, "QBTS": 20, "INFQ": 10,
    # Drones
    "ONDS": 7, "AVAV": 174, "KTOS": 52, "MRCY": 104,
    # Nuclear
    "OKLO": 50, "UUUU": 12, "GEV": 906, "LEU": 132,
    # Photonics
    "AAOI": 103, "LITE": 636, "COHR": 311, "AEHR": 59,
    # CPU
    "AMD": 515, "INTC": 120, "ARM": 304, "AMKR": 64,
    # Physical AI
    "TSLA": 382, "AMZN": 230, "GOOGL": 357, "ISRG": 397,
    # AI Utilities
    "IREN": 31, "NBIS": 213, "CIFR": 17, "CRWV": 67,
    # AI Power
    "EOSE": 4, "BE": 265, "NVTS": 13, "VRT": 282,
    # AI Connectivity
    "AVGO": 334, "ALAB": 341, "CRDO": 210, "MRVL": 225,
    # AI Hardware
    "NVDA": 192, "TSM": 419, "ASML": 1732, "MU": 869,
    # AI Applications
    "PLTR": 121, "NOW": 104, "CRWD": 171, "SNOW": 181,
}

# ── Sector groups (for dashboard Sectors panel) ───────────────────────────────
SECTOR_GROUPS: dict[str, list[str]] = {
    "Space":          ["RKLB", "ASTS", "PL", "RDW"],
    "Quantum":        ["IONQ", "RGTI", "QBTS", "INFQ"],
    "Drones":         ["ONDS", "AVAV", "KTOS", "MRCY"],
    "Nuclear":        ["OKLO", "UUUU", "GEV", "LEU"],
    "Photonics":      ["AAOI", "LITE", "COHR", "AEHR"],
    "CPU":            ["AMD", "INTC", "ARM", "AMKR"],
    "Physical AI":    ["TSLA", "AMZN", "GOOGL", "ISRG"],
    "AI Utilities":   ["IREN", "NBIS", "CIFR", "CRWV"],
    "AI Power":       ["EOSE", "BE", "NVTS", "VRT"],
    "AI Connectivity":["AVGO", "ALAB", "CRDO", "MRVL"],
    "AI Hardware":    ["NVDA", "TSM", "ASML", "MU"],
    "AI Applications":["PLTR", "NOW", "CRWD", "SNOW"],
}

# ── RSI parameters ───────────────────────────────────────────────────────────
RSI_PERIOD = 14
RSI_OVERSOLD = 30              # buy signal threshold — tighter entry, avoids mid-drop knives
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

# ── Circuit breakers ──────────────────────────────────────────────────────────
# Halt all new buys if account drops this much from prior reference value.
# CCR writes peak_value + week_start_value to positions.json each cycle.
DAILY_LOSS_HALT   = 0.03   # 3 % drop from prior-day close → no new buys today
WEEKLY_LOSS_HALT  = 0.05   # 5 % drop from Monday open → no new buys this week
CONCENTRATION_MAX = 0.20   # single-position value / account_value ceiling (= $20 / $100)

# ── Momentum signal thresholds ────────────────────────────────────────────────
# Catches EMA-trending stocks with elevated volume (e.g. META) — complements RSI mean-reversion
MOMENTUM_RSI_MIN = 45   # must have some upside momentum already
MOMENTUM_RSI_MAX = 62   # not yet overbought
MOMENTUM_VOL_MIN = 1.3  # volume ≥ 30% above 20-bar average confirms real buying interest

# ── Market data ───────────────────────────────────────────────────────────────
DATA_PERIOD = "60d"            # lookback window for indicator warmup
DATA_INTERVAL = "1h"           # 1-hour bars
VOLUME_LOOKBACK = 20           # days for avg-volume filter

# ── Market regime filter ──────────────────────────────────────────────────────
# RSI panic filter (extreme only)
MARKET_REGIME_RSI_MIN = 30
# 200-period EMA regime: if SPY close < SPY EMA200 → bearish trend
# Effect: max position $10 (halved), require 3/3 signal confidence
EMA200_PERIOD = 200
BEARISH_EMA_MAX_POSITION = 10.0   # halved from MAX_POSITION_SIZE
BEARISH_EMA_MIN_CONFIDENCE = 3    # require 3/3 vs normal 2/3

# ── ATR trailing stop ─────────────────────────────────────────────────────────
ATR_STOP_MULTIPLIER = 2.0   # initial stop = entry − ATR_STOP_MULTIPLIER × ATR (wider = less whipsaw on hourly bars)
MIN_HOLD_BARS = 3           # don't fire ATR stop in first N bars — gives trade room to breathe
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
