"""Hard account-level kill switch, shared by the equity and options systems.

Different from DAILY_LOSS_HALT / WEEKLY_LOSS_HALT in config.py, which reset
every day/week. This one does not reset itself -- once account_value drops
ACCOUNT_KILL_SWITCH_PCT below TOTAL_CAPITAL, it flips trading_enabled to
false in docs/positions.json and stays there across runs until a human
reviews the account and flips it back manually.
"""
import json
from pathlib import Path

from .config import TOTAL_CAPITAL, ACCOUNT_KILL_SWITCH_PCT

STATE_FILE = Path("docs/positions.json")


def check(account_value: float | None = None, state_file: Path = STATE_FILE) -> tuple[bool, str]:
    """Returns (trading_allowed, reason).

    Pass the latest account_value (from get_portfolio) each cycle so a fresh
    drawdown can trip the switch. Omit it to just read the persisted state.
    """
    state = {}
    if state_file.exists():
        try:
            state = json.loads(state_file.read_text())
        except (json.JSONDecodeError, OSError):
            state = {}

    if state.get("trading_enabled") is False:
        return False, state.get("disabled_reason") or "trading_enabled=false in docs/positions.json"

    if account_value is None:
        account_value = state.get("account_value")
    if account_value is None:
        return True, ""

    floor = TOTAL_CAPITAL * (1 - ACCOUNT_KILL_SWITCH_PCT)
    if account_value <= floor:
        reason = (
            f"Kill switch tripped: account value ${account_value:.2f} <= floor "
            f"${floor:.2f} ({ACCOUNT_KILL_SWITCH_PCT:.0%} drawdown from "
            f"${TOTAL_CAPITAL:.0f}). Set trading_enabled=true in docs/positions.json "
            "to resume, manually, after review."
        )
        state["trading_enabled"] = False
        state["disabled_reason"] = reason
        state["account_value"] = account_value
        state_file.parent.mkdir(exist_ok=True)
        state_file.write_text(json.dumps(state, indent=2))
        return False, reason

    return True, ""


def demo():
    import tempfile
    tmp = Path(tempfile.mkdtemp()) / "positions.json"

    ok, reason = check(300.0, state_file=tmp)
    assert ok and reason == "", "above floor should pass"
    ok, reason = check(150.0, state_file=tmp)
    assert not ok and "Kill switch tripped" in reason, "below floor should trip"
    ok2, reason2 = check(300.0, state_file=tmp)
    assert not ok2 and reason2 == reason, "tripped state should persist even if value recovers"
    print("circuit_breaker.demo: OK (trips below floor, stays tripped until manual reset)")


if __name__ == "__main__":
    demo()
