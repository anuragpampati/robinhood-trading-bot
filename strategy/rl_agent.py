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
ALPHA  = 0.20   # faster learning — more data per state now
GAMMA  = 0.75   # weight immediate trade P&L over distant future
EPSILON_START = 0.15
EPSILON_MIN   = 0.02
EPSILON_DECAY = 0.990

ACTIONS = ["BUY", "HOLD", "SELL"]

# State: 4 dimensions (removed bb_signal and vol_bucket — always constant in our signals)
# RSI: 6 buckets with finer resolution in the <35 oversold zone where edge lives
# ATR: 3 buckets — distinguishes calm/normal/volatile entries
# Possible states: 6 × 3 × 3 × 2 = 108  (vs old 5×3×3×3×2×2 = 540 with only 13 visited)


@dataclass
class State:
    rsi_bucket: str   # deep(<25) / oversold(25-30) / low(30-38) / mid(38-55) / high(55-70) / ob(70+)
    ema:        str   # BULLISH / BEARISH / NEUTRAL
    atr_bucket: str   # low(<0.01) / mid(0.01-0.025) / high(>0.025)
    regime:     str   # normal / bearish_ema

    def key(self) -> str:
        return "|".join(asdict(self).values())


def _bucket_rsi(rsi: float) -> str:
    if rsi < 25:  return "deep"
    if rsi < 30:  return "oversold"
    if rsi < 38:  return "low"
    if rsi < 55:  return "mid"
    if rsi < 70:  return "high"
    return "ob"


def _bucket_atr(atr_pct: float) -> str:
    if atr_pct < 0.010:  return "low"
    if atr_pct < 0.025:  return "mid"
    return "high"


def make_state(obs: dict) -> State:
    return State(
        rsi_bucket = _bucket_rsi(obs.get("rsi", 50)),
        ema        = obs.get("ema_trend", "NEUTRAL"),
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
        if k not in self.q:
            return "HOLD", 0.0  # unknown state → no opinion
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
            # Reward shaping: penalise high-ATR losing BUY entries more —
            # they're the most avoidable (chasing volatile moves)
            if action == "BUY" and reward < 0:
                atr = row["obs"].get("atr_pct", 0.01)
                if atr > 0.025:
                    reward *= 1.5   # amplify penalty on volatile losers
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
