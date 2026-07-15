"""
Options system shared constants — imported by options_engine, options_backtest, and CCR.

Signal generation has moved to strategy/options_engine.py (independent daily-bar system).
This file exists only so backtest and CCR can share the same risk parameters without
importing the full engine.
"""

# Tickers: liquid options where 1 contract costs ≤$75 at 14 DTE, ~5.5% OTM
OPTIONS_TICKERS = ["NVDA", "AAPL", "AMZN", "META"]

MAX_SPEND        = 75.0   # max premium per 1-contract purchase ($)
MAX_POSITIONS    = 2      # max concurrent positions across all tickers
TARGET_DTE       = 14     # target days-to-expiry when opening
OTM_PCT          = 0.055  # ~5.5% OTM for strike selection
TAKE_PROFIT_PCT  = 0.50   # close when premium gained +50%
STOP_LOSS_PCT    = 0.50   # close when premium lost -50%
MIN_DTE          = 5      # force-close at or below this DTE
