"""Options trade idea generator — derives option direction from equity signals.

Only generates ideas for tickers where a single contract can be bought for
≤$75. Budget reality check (approximate contract cost at typical ATM, 14 DTE):
  NVDA  ~$130  → OTM call/put ~$20-40  ✓
  AAPL  ~$210  → OTM call/put ~$15-35  ✓
  AMZN  ~$220  → OTM call/put ~$20-40  ✓
  META  ~$600  → OTM call/put ~$30-60  ✓ (5% OTM keeps it in range)
  MSFT  ~$470  → OTM call/put ~$40-80  ✗ often over budget — removed
  QQQ   ~$515  → OTM call/put ~$150+   ✗ way over budget — removed

Risk profile: long options only. Max loss = premium paid (~$75). No spreads,
no naked selling. Options supplement equity positions; never the primary bet.
"""

# Tickers confirmed affordable at 5% OTM, 14 DTE for ≤$75/contract
OPTIONS_TICKERS = {"NVDA", "AAPL", "AMZN", "META"}

MAX_SPEND         = 75.0   # max premium per 1-contract purchase ($)
MAX_POSITIONS     = 2      # max concurrent option positions across all tickers
TARGET_DTE_MIN    = 10     # minimum DTE when opening
TARGET_DTE_MAX    = 21     # maximum DTE when opening
TARGET_DELTA      = 0.35   # slightly OTM — affordable, still meaningful edge
TAKE_PROFIT_PCT   = 0.50   # close at +50% gain on premium paid
STOP_LOSS_PCT     = 0.50   # close at -50% loss on premium paid
MIN_DTE_TO_HOLD   = 5      # force-close to avoid pin risk and theta cliff

# Minimum confidence to generate an idea:
# conf=2 → standard (2 of 3 indicators aligned)
# conf=1 → relaxed tier — only generated if signal is extreme (RSI<25 or RSI>75)
MIN_CONFIDENCE = 2


def generate_options_idea(ticker: str, action: str, confidence: int,
                          rsi: float = 50.0) -> dict | None:
    """Return an options trade idea dict, or None if no trade warranted.

    Args:
        ticker:     equity symbol
        action:     "BUY" | "SELL" | "HOLD" from RSI/EMA/BB signal
        confidence: 0-3 aligned indicator count
        rsi:        current RSI value (used for relaxed-tier check)
    """
    if ticker not in OPTIONS_TICKERS:
        return None
    if action not in ("BUY", "SELL"):
        return None

    # Standard tier: 2+ indicators aligned
    # Relaxed tier: 1 indicator + extreme RSI (RSI<25 for calls, RSI>75 for puts)
    extreme_rsi = (action == "BUY" and rsi < 25) or (action == "SELL" and rsi > 75)
    if confidence < MIN_CONFIDENCE and not (confidence >= 1 and extreme_rsi):
        return None

    opt_type = "call" if action == "BUY" else "put"
    tier = "standard" if confidence >= MIN_CONFIDENCE else "relaxed"

    return {
        "ticker":       ticker,
        "option_type":  opt_type,
        "target_delta": TARGET_DELTA,
        "dte_min":      TARGET_DTE_MIN,
        "dte_max":      TARGET_DTE_MAX,
        "max_spend":    MAX_SPEND,
        "take_profit":  TAKE_PROFIT_PCT,
        "stop_loss":    STOP_LOSS_PCT,
        "min_dte_hold": MIN_DTE_TO_HOLD,
        "tier":         tier,
        "reason":       f"{action} conf={confidence} rsi={rsi:.1f} → buy {opt_type} [{tier}]",
    }
