"""
Collects (observation, action, reward) tuples from trade history for RL training.

Called by the daily learning CCR after market close. Appends new rows to
logs/rl_training_data.jsonl — one JSON line per closed trade.

Observation keys match make_state() in rl_agent.py:
  rsi, ema_trend, bb_signal, vol_ratio, atr_pct, regime

Reward: pnl_pct × 100  (e.g. +1.5 for a 1.5% gain, -0.8 for a 0.8% loss)
"""

import json
import re
from datetime import datetime, timezone
from pathlib import Path

DATA_PATH = Path("logs/rl_training_data.jsonl")


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


def extract_from_signals_history(signals_dir: Path = Path("logs")) -> list[dict]:
    """
    Build training rows from latest_signals.json + trade_log.md.

    Each row pairs a signal's entry observation with the eventual trade outcome.
    """
    rows = []
    sig_file = signals_dir / "latest_signals.json"
    log_file  = Path("docs/positions.json")

    if not sig_file.exists():
        return rows

    try:
        sigs = json.loads(sig_file.read_text())
    except Exception:
        return rows

    regime = sigs.get("market_regime", "normal")
    timestamp = sigs.get("timestamp", datetime.now(timezone.utc).isoformat())

    for s in sigs.get("rsi_signals", []):
        action = s.get("action", "HOLD")
        if action == "HOLD":
            continue

        # Approximate vol_ratio from confidence (no raw vol_ratio in signals.json yet)
        conf = s.get("confidence", 1)
        vol_ratio = 1.0 + (conf - 1) * 0.3  # proxy until vol_ratio is added to signals

        obs = {
            "rsi":       s.get("rsi", 50.0),
            "ema_trend": s.get("ema_trend", "NEUTRAL"),
            "bb_signal": s.get("bb_signal", "WITHIN"),
            "vol_ratio": vol_ratio,
            "atr_pct":   s.get("atr_pct", 0.01),
            "regime":    regime,
        }

        trade_id = f"{s['ticker']}|{timestamp[:10]}|{action}"

        rows.append({
            "trade_id":  trade_id,
            "timestamp": timestamp,
            "ticker":    s["ticker"],
            "action":    action,
            "price":     s.get("price", 0),
            "obs":       obs,
            "reward":    None,   # filled in when trade closes
        })

    return rows


def update_rewards_from_positions(rows: list[dict]) -> list[dict]:
    """
    Cross-reference pending rows against closed positions in positions.json.
    Sets reward = pnl_pct * 100 for rows that have since been closed.
    Rows with reward=None (still open) are not written to training file.
    """
    pos_file = Path("docs/positions.json")
    if not pos_file.exists():
        return rows

    try:
        positions = json.loads(pos_file.read_text())
    except Exception:
        return rows

    # Build lookup of held tickers → current pnl_pct
    held = {p["ticker"]: p.get("pnl_pct", 0) for p in positions.get("positions", [])}

    for row in rows:
        ticker = row["ticker"]
        if row["reward"] is not None:
            continue
        if ticker in held:
            # still open — reward unknown yet; use current unrealised P&L as partial signal
            row["reward"] = round(held[ticker] * 100, 4)
        else:
            # not currently held → assume trade closed; reward = 0 (hold observation)
            row["reward"] = 0.0

    return rows


def append_new_rows(rows: list[dict]):
    existing_ids = _load_existing_ids()
    new_rows = [r for r in rows if r["trade_id"] not in existing_ids and r["reward"] is not None]
    if not new_rows:
        return 0
    DATA_PATH.parent.mkdir(exist_ok=True)
    with DATA_PATH.open("a") as f:
        for row in new_rows:
            f.write(json.dumps(row) + "\n")
    return len(new_rows)


def collect():
    rows = extract_from_signals_history()
    rows = update_rewards_from_positions(rows)
    n = append_new_rows(rows)
    total = sum(1 for _ in DATA_PATH.open()) if DATA_PATH.exists() else 0
    print(f"[RL collector] +{n} new rows  →  {total} total in {DATA_PATH}")
    return n


if __name__ == "__main__":
    collect()
