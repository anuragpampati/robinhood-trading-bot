"""Options trade idea generator — derives option direction from equity signals.

Only generates ideas for the most liquid, optionable tickers where $75/contract
buys a near-ATM option. Actual strike/expiry selection happens at execution time
via live option chain data (requires MCP).

Risk profile: long options only. Max loss = premium paid (~$75). No spreads,
no naked selling. Appropriate for a $500 account where options are a supplement
to equity positions, not the primary strategy.
"""

# Tickers with liquid options and single-contract premiums under $75 at typical ATM
OPTIONS_TICKERS = {"NVDA", "AAPL", "MSFT", "AMZN", "META", "QQQ"}

MAX_SPEND         = 75.0  # max premium per 1-contract purchase
MAX_POSITIONS     = 2     # max concurrent option positions across all tickers
TARGET_DTE_MIN    = 10    # minimum DTE when opening a position
TARGET_DTE_MAX    = 21    # maximum DTE when opening a position
TARGET_DELTA      = 0.35  # slightly OTM — keeps premium in budget, still has edge
TAKE_PROFIT_PCT   = 0.50  # close at +50% gain on premium paid
STOP_LOSS_PCT     = 0.50  # close at -50% loss on premium paid
MIN_DTE_TO_HOLD   = 5     # force-close when DTE falls below this (avoid pin risk)


def generate_options_idea(ticker: str, action: str, confidence: int) -> dict | None:
    """Return an options trade idea dict, or None if no trade warranted.

    Args:
        ticker:     equity symbol
        action:     "BUY" | "SELL" | "HOLD" from equity RSI/EMA/BB signal
        confidence: 0–3 indicator count aligned
    """
    if ticker not in OPTIONS_TICKERS:
        return None
    if confidence < 2:
        return None
    if action == "BUY":
        option_type = "call"
    elif action == "SELL":
        option_type = "put"
    else:
        return None

    return {
        "ticker":       ticker,
        "option_type":  option_type,   # "call" or "put"
        "target_delta": TARGET_DELTA,
        "dte_min":      TARGET_DTE_MIN,
        "dte_max":      TARGET_DTE_MAX,
        "max_spend":    MAX_SPEND,
        "take_profit":  TAKE_PROFIT_PCT,
        "stop_loss":    STOP_LOSS_PCT,
        "min_dte_hold": MIN_DTE_TO_HOLD,
        "reason":       f"{action} signal (conf={confidence}) → buy {option_type}",
    }
