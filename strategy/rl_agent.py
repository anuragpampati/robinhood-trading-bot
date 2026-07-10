"""
Reinforcement Learning agent scaffold for the Robinhood trading strategy.

Architecture: Tabular Q-learning (state → action → expected reward).
State is discretised from RSI, EMA trend, BB position, vol ratio, ATR, regime.
Q-table is stored as a JSON file so it's human-readable and survives restarts.

DO NOT ACTIVATE until ~30 days of training data exist in logs/rl_training_data.jsonl.
Invoke training: python -m strategy.rl_agent --train
Invoke prediction: python -m strategy.rl_agent --predict --ticker NVDA
"""

import json
import math
import random
import sys
from pathlib import Path
from dataclasses import dataclass, asdict

Q_TABLE_PATH = Path("logs/q_table.json")
DATA_PATH     = Path("logs/rl_training_data.jsonl")

# Hyper-parameters
ALPHA  = 0.10   # learning rate
GAMMA  = 0.90   # discount factor (we care about near-term P&L)
EPSILON_START = 0.20
EPSILON_MIN   = 0.02
EPSILON_DECAY = 0.995

ACTIONS = ["BUY", "HOLD", "SELL"]


@dataclass
class State:
    rsi_bucket:    str   # oversold / low / mid / high / overbought
    ema:           str   # BULLISH / BEARISH / NEUTRAL
    bb:            str   # BELOW_BAND / WITHIN / ABOVE_BAND
    vol_bucket:    str   # low / normal / high
    atr_bucket:    str   # low / high
    regime:        str   # normal / bearish_ema

    def key(self) -> str:
        return "|".join(asdict(self).values())


def _bucket_rsi(rsi: float) -> str:
    if rsi < 30:   return "oversold"
    if rsi < 45:   return "low"
    if rsi < 55:   return "mid"
    if rsi < 70:   return "high"
    return "overbought"


def _bucket_vol(vol_ratio: float) -> str:
    if vol_ratio < 0.8:  return "low"
    if vol_ratio < 1.3:  return "normal"
    return "high"


def _bucket_atr(atr_pct: float) -> str:
    return "high" if atr_pct > 0.015 else "low"


def make_state(obs: dict) -> State:
    return State(
        rsi_bucket = _bucket_rsi(obs.get("rsi", 50)),
        ema        = obs.get("ema_trend", "NEUTRAL"),
        bb         = obs.get("bb_signal", "WITHIN"),
        vol_bucket = _bucket_vol(obs.get("vol_ratio", 1.0)),
        atr_bucket = _bucket_atr(obs.get("atr_pct", 0.01)),
        regime     = obs.get("regime", "normal"),
    )


class QAgent:
    def __init__(self, epsilon: float = EPSILON_START):
        self.q: dict[str, dict[str, float]] = {}
        self.epsilon = epsilon
        if Q_TABLE_PATH.exists():
            self.q = json.loads(Q_TABLE_PATH.read_text())

    def _q(self, state_key: str, action: str) -> float:
        return self.q.get(state_key, {}).get(action, 0.0)

    def best_action(self, state: State) -> tuple[str, float]:
        k = state.key()
        scores = {a: self._q(k, a) for a in ACTIONS}
        best = max(scores, key=scores.__getitem__)
        return best, scores[best]

    def choose(self, state: State) -> str:
        """Epsilon-greedy action selection."""
        if random.random() < self.epsilon:
            return random.choice(ACTIONS)
        return self.best_action(state)[0]

    def update(self, state: State, action: str, reward: float, next_state: State):
        k  = state.key()
        nk = next_state.key()
        old_q    = self._q(k, action)
        best_nq  = max(self._q(nk, a) for a in ACTIONS)
        new_q    = old_q + ALPHA * (reward + GAMMA * best_nq - old_q)
        self.q.setdefault(k, {})[action] = round(new_q, 6)

    def save(self):
        Q_TABLE_PATH.parent.mkdir(exist_ok=True)
        Q_TABLE_PATH.write_text(json.dumps(self.q, indent=2))

    def decay_epsilon(self):
        self.epsilon = max(EPSILON_MIN, self.epsilon * EPSILON_DECAY)


def train(epochs: int = 3):
    if not DATA_PATH.exists():
        print(f"[RL] No training data at {DATA_PATH}. Collect more data first.")
        return

    rows = [json.loads(l) for l in DATA_PATH.read_text().splitlines() if l.strip()]
    if len(rows) < 30:
        print(f"[RL] Only {len(rows)} samples — need ≥30.")
        return

    agent = QAgent(epsilon=EPSILON_START)
    for epoch in range(epochs):
        random.shuffle(rows)
        total_reward = 0.0
        for i, row in enumerate(rows[:-1]):
            state      = make_state(row["obs"])
            action     = row["action"]
            reward     = float(row["reward"])
            next_state = make_state(rows[i + 1]["obs"])
            agent.update(state, action, reward, next_state)
            total_reward += reward
        agent.decay_epsilon()
        print(f"  Epoch {epoch+1}/{epochs} — avg reward {total_reward/len(rows):+.4f}  ε={agent.epsilon:.3f}")

    agent.save()
    print(f"[RL] Q-table saved → {Q_TABLE_PATH}  ({len(agent.q)} states learned)")


def predict(obs: dict) -> tuple[str, float]:
    """Return (action, confidence) for a live signal observation."""
    if not Q_TABLE_PATH.exists():
        return "HOLD", 0.0
    agent = QAgent(epsilon=0.0)
    state = make_state(obs)
    action, score = agent.best_action(state)
    # normalise score to [0,1] confidence using sigmoid
    confidence = 1 / (1 + math.exp(-score))
    return action, round(confidence, 3)


if __name__ == "__main__":
    if "--train" in sys.argv:
        epochs = int(sys.argv[sys.argv.index("--epochs") + 1]) if "--epochs" in sys.argv else 3
        train(epochs)
    elif "--predict" in sys.argv:
        # quick smoke-test with a sample observation
        obs = {"rsi": 28, "ema_trend": "BULLISH", "bb_signal": "BELOW_BAND",
               "vol_ratio": 1.5, "atr_pct": 0.012, "regime": "normal"}
        action, conf = predict(obs)
        print(f"Sample obs → {action}  confidence={conf:.1%}")
    else:
        print(__doc__)
