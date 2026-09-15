"""
Collects (observation, action, reward) tuples from REAL executed trades for RL
training. Called by the daily learning CCR after market close, before
trim_log.py trims logs/trade_log.md -- runs once/day so every trade gets
processed while it's still in the (2-day-trimmed) log.

Was previously building rows from logs/latest_signals.json (every computed
signal, whether or not a trade was actually placed) and guessing reward=0.0
for any ticker not currently held -- which conflated "signal fired" with
"trade executed" and was wrong for the common case of a position that closed
profitably or at a loss before the next collection run. Real money trades are
BOOST/VETO'd by this model's predictions, so a corrupted reward signal was a
real problem, not a cosmetic one. Rewritten to pair actual BUY -> SELL entries
from trade_log.md (mirrors backtest.py --export-rl's approach exactly) and
compute the real realized P&L.

Observation keys match make_state() in rl_agent.py: rsi, ema_trend, atr_pct,
regime. atr_pct isn't logged directly -- trade_log.md logs the entry Stop
price, and back_derived from it via config.ATR_STOP_MULTIPLIER (same formula
backtest.py uses to set the initial stop).

Reward: pnl_pct * 100 (e.g. +1.5 for a 1.5% gain, -0.8 for a 0.8% loss).
"""

import json
import re
from pathlib import Path

from .config import ATR_STOP_MULTIPLIER

DATA_PATH  = Path("logs/rl_training_data.jsonl")
TRADE_LOG  = Path("logs/trade_log.md")

_ACTION_RE = re.compile(r"^-\s*Action\s*:\s*(BUY|SELL)\s+(\S+)", re.M)
_PRICE_RE  = re.compile(r"^-\s*Price\s*:\s*\$([\d.]+)", re.M)
_RSI_RE    = re.compile(r"^-\s*RSI\s*:\s*([\d.]+)\s*\|\s*EMA:\s*(\w+)", re.M)
_STOP_RE   = re.compile(r"^-\s*Stop\s*:\s*\$([\d.]+)", re.M)
_REGIME_RE = re.compile(r"^-\s*Regime\s*:\s*(\w+)", re.M)


def _load_existing_ids() -> set[str]:
    if not DATA_PATH.exists():
        return set()
    ids = set()
    for line in DATA_PATH.read_text().splitlines():
        try:
            ids.add(json.loads(line)["trade_id"])
        except Exception:
            pass
    return ids


def _parse_trade_log(path: Path = TRADE_LOG) -> list[dict]:
    """Parse logs/trade_log.md into BUY/SELL entries, oldest first.

    Entries are prepended at the top of the file (newest first), so the
    parsed list is reversed before returning.
    """
    if not path.exists():
        return []
    chunks = path.read_text().split("\n## ")[1:]  # [0] is the file preamble

    entries = []
    for chunk in chunks:
        lines = chunk.split("\n", 1)
        timestamp = lines[0].strip()
        body = lines[1] if len(lines) > 1 else ""

        m_action = _ACTION_RE.search(body)
        m_price = _PRICE_RE.search(body)
        if not m_action or not m_price:
            continue  # a no-trade SUMMARY entry, not a trade

        side, ticker = m_action.groups()
        entry = {"timestamp": timestamp, "side": side, "ticker": ticker,
                 "price": float(m_price.group(1))}

        m_rsi = _RSI_RE.search(body)
        if m_rsi:
            entry["rsi"] = float(m_rsi.group(1))
            entry["ema_trend"] = m_rsi.group(2)

        m_stop = _STOP_RE.search(body)
        if m_stop:
            entry["stop"] = float(m_stop.group(1))

        m_regime = _REGIME_RE.search(body)
        entry["regime"] = m_regime.group(1) if m_regime else "normal"

        entries.append(entry)

    entries.reverse()  # oldest first
    return entries


def _pair_trades(entries: list[dict]) -> list[tuple[dict, dict]]:
    """Match each BUY to the next SELL of the same ticker. Still-open
    positions (a BUY with no matching SELL yet) are left unpaired -- no
    training row until the trade actually closes."""
    open_buys: dict[str, dict] = {}
    pairs = []
    for e in entries:
        if e["side"] == "BUY":
            open_buys[e["ticker"]] = e
        elif e["side"] == "SELL" and e["ticker"] in open_buys:
            pairs.append((open_buys.pop(e["ticker"]), e))
    return pairs


def _row_from_pair(buy: dict, sell: dict) -> dict | None:
    if "rsi" not in buy or buy["price"] <= 0:
        return None  # entry predates the RSI/EMA logging fields, can't build an obs

    atr_pct = 0.01
    if "stop" in buy:
        atr_pct = max((buy["price"] - buy["stop"]) / (buy["price"] * ATR_STOP_MULTIPLIER), 0.001)

    obs = {
        "rsi": buy["rsi"],
        "ema_trend": buy["ema_trend"],
        "atr_pct": round(atr_pct, 4),
        "regime": buy.get("regime", "normal"),
    }
    reward = round((sell["price"] - buy["price"]) / buy["price"] * 100, 4)

    return {
        "trade_id": f"{buy['ticker']}|{buy['timestamp']}|LIVE",
        "timestamp": buy["timestamp"],
        "ticker": buy["ticker"],
        "action": "BUY",
        "price": buy["price"],
        "obs": obs,
        "reward": reward,
    }


def append_new_rows(rows: list[dict]) -> int:
    existing_ids = _load_existing_ids()
    new_rows = [r for r in rows if r["trade_id"] not in existing_ids]
    if not new_rows:
        return 0

    # Counterfactual HOLD row for losing trades: teaches the model "not
    # buying = 0 loss", same technique backtest.py --export-rl already uses.
    out_rows = list(new_rows)
    for r in new_rows:
        if r["reward"] < 0:
            out_rows.append({**r, "trade_id": r["trade_id"] + "|HOLD",
                             "action": "HOLD", "reward": 0.0})

    DATA_PATH.parent.mkdir(exist_ok=True)
    with DATA_PATH.open("a") as f:
        for row in out_rows:
            f.write(json.dumps(row) + "\n")
    return len(out_rows)


def collect() -> int:
    entries = _parse_trade_log()
    pairs = _pair_trades(entries)
    rows = [r for r in (_row_from_pair(b, s) for b, s in pairs) if r is not None]
    n = append_new_rows(rows)
    total = sum(1 for _ in DATA_PATH.open()) if DATA_PATH.exists() else 0
    print(f"[RL collector] +{n} new rows ({len(pairs)} closed trades found)  →  {total} total in {DATA_PATH}")
    return n


def demo():
    """Self-check: a synthetic BUY->SELL pair produces the expected reward.
    Written newest-first, matching trade_log.md's real prepend convention."""
    text = (
        "# header\n"
        "## 2026-01-02T00:00:00Z\n"
        "- Action   : SELL TEST\n"
        "- Price    : $110.00\n"
        "- RSI      : 60.0 | EMA: BULLISH | BB: IN_BAND\n"
        "- Stop     : $96.00\n"
        "- Regime   : normal\n"
        "## 2026-01-01T00:00:00Z\n"
        "- Action   : BUY TEST\n"
        "- Price    : $100.00\n"
        "- RSI      : 25.0 | EMA: BULLISH | BB: BELOW_BAND\n"
        "- Stop     : $96.00\n"
        "- Regime   : normal\n"
    )
    import tempfile
    tmp = Path(tempfile.mkdtemp()) / "trade_log.md"
    tmp.write_text(text)

    entries = _parse_trade_log(tmp)
    assert len(entries) == 2, f"expected 2 entries, got {len(entries)}"
    assert entries[0]["side"] == "BUY" and entries[1]["side"] == "SELL", "wrong order"

    pairs = _pair_trades(entries)
    assert len(pairs) == 1, f"expected 1 pair, got {len(pairs)}"

    row = _row_from_pair(*pairs[0])
    assert row is not None
    assert abs(row["reward"] - 10.0) < 0.01, f"expected reward ~10.0, got {row['reward']}"
    assert row["obs"]["atr_pct"] == 0.02, f"expected atr_pct 0.02 ((100-96)/(100*2)), got {row['obs']['atr_pct']}"

    print("rl_collector.demo: OK (BUY $100 -> SELL $110 pairs to reward=+10.0)")


if __name__ == "__main__":
    if "--demo" in __import__("sys").argv:
        demo()
    else:
        collect()
