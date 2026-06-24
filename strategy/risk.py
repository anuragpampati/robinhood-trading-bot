"""Risk calculations for trade logging."""

from .config import STOP_LOSS_PCT, TAKE_PROFIT_PCT


def risk_summary(entry_price: float, dollar_amount: float) -> dict:
    sl = round(entry_price * (1 - STOP_LOSS_PCT), 4)
    tp = round(entry_price * (1 + TAKE_PROFIT_PCT), 4)
    risk = entry_price - sl
    return {
        "stop_loss": sl,
        "take_profit": tp,
        "risk_reward": round((tp - entry_price) / risk, 2) if risk > 0 else 0,
    }
