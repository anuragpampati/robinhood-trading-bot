# Learning Log — Robinhood Agentic Account

> Auto-maintained by daily learning CCR agent.

---

## 2026-07-23
- Trades analysed: 9 closed (same as prior day — no new exits); 1 open (PLTR -0.21%, bearish_ema regime)
- Win rate: 55.6% overall (normal: 55.6% — 5W/4L, avg_pnl +0.07%, avg_hold ~182h; momentum: n/a — 0 trades; surge: n/a — 0 trades)
- EMA-trend win rate: BULLISH entry 55.6% (9/9 closed trades); BEARISH entry n/a (0 closed — PLTR bearish entry still open)
- Config changes: none — RSI_OVERSOLD: win_rate=55.6% in [40%,65%] range, NO_CHANGE (n=9≥5); MOMENTUM_VOL_MIN: no momentum entries (n<3), NO_CHANGE; ATR_VOLATILITY_THRESHOLD: avg_hold ~182h >> 2h, NO_CHANGE
- Backtest: SKIPPED — yfinance proxy blocked (403). Prior 365d metrics retained: +9.29% return, 15.3% drawdown, 39.6% win rate
- RL samples: 407/200 (READY — +6 new rows today; 19 states in Q-table)
- Notes: No new exits today. PLTR entered 2026-07-23 at $123.53, bearish_ema regime, $50 position. Market in PANIC (SPY RSI <30) + bearish_ema most of the day. Account $100.14, peak $101.68. Buying power $50.24 (at buffer limit). RL exceeds 200 target — run: python -m strategy.rl_agent --train

## 2026-07-22
- Trades analysed: 9 closed (RKLB +2.93%, SMCI +2.41%, GS -2.46%, DELL -6.01%, DKNG +0.71%, AUR -4.10%, WMT +5.28%, DIS -2.28%, JPM +4.13%); 0 open
- Win rate: 55.6% overall (normal: 55.6% — 5W/4L, avg_pnl +0.07%, avg_hold ~182h; momentum: n/a — 0 trades; surge: n/a — 0 trades)
- EMA-trend win rate: BULLISH entry 55.6% (9/9 trades); BEARISH entry n/a (0 trades)
- Config changes: none — RSI_OVERSOLD: win_rate=55.6% in [40%,65%] range, NO_CHANGE (n=9≥5); MOMENTUM_VOL_MIN: no momentum entries (n<3), NO_CHANGE; ATR_VOLATILITY_THRESHOLD: avg_hold ~182h >> 2h, NO_CHANGE
- Backtest: SKIPPED — yfinance proxy blocked (403). Prior 365d metrics retained: +9.29% return, 15.3% drawdown, 39.6% win rate
- RL samples: 401/200 (READY — +6 new rows today; 19 states in Q-table)
- Notes: JPM closed today +4.13% via signal sell (net-buy reversal + OBV decline). Account $100.24 — above $100 start. No open equity positions; buying power $84.62 (cash-buffer bind preventing new entries at $50 order size). 3 strong RSI buy candidates visible after hours: PLTR, GEV, NOW. Log trimmed to 10 entries.

## 2026-07-15
- Trades analysed: 3 closed (DELL -6.01%, DKNG +0.71%, AUR -4.10%; 2 open: WMT/JPM)
- Win rate: 33.3% overall (normal: 33.3% — 1W/2L; momentum: n/a — 0 trades; surge: n/a — 0 trades)
- Config changes: none — RSI_OVERSOLD: n=3 < 5 (need ≥5); MOMENTUM_VOL_MIN: no momentum-strategy closed trades (n<3); ATR_VOLATILITY_THRESHOLD: avg_hold ~140h > 2h, rule not triggered
- Backtest: SKIPPED — yfinance proxy blocked (403). Prior metrics retained: +9.29% 365d return, 15.3% drawdown, 39.6% win rate
- RL samples: 380/200 (READY — +4 new rows collected today; 19 states in Q-table)
- Notes: AUR exited 2026-07-15 at -4.1% via ATR trailing stop (held ~48h). RKLB sold between 2026-07-14T18:11 and 2026-07-15T15:15 (explicit entry trimmed from log). WMT +1.8%/JPM +4.2% still held. Account $100.11. Log trimmed to 12 entries. RL exceeds 200 target — ready to train Q-agent.

## 2026-07-13
- Trades analysed: 4 cumulative closed (SMCI +2.41%, GS -2.46%, RKLB +2.93%, DELL -6.01%; 4 open: WMT/DKNG/JPM/AUR)
- Win rate: 50.0% overall (normal: 50.0% — 2W/2L; momentum: n/a — 0 trades; surge: n/a — 0 trades)
- Config changes: none — RSI_OVERSOLD: n=4 < 5 (need ≥5); MOMENTUM_VOL_MIN: no momentum-strategy closed trades (n<3); ATR_VOLATILITY_THRESHOLD: avg_hold ~53h > 2h threshold, rule not triggered
- Backtest: SKIPPED — yfinance proxy blocked (403). Prior metrics retained: +9.29% 365d return, 15.3% drawdown, 39.6% win rate
- RL samples: 376/200 (READY — exceeds target; +10 new rows collected today)
- Notes: DELL exited at -6.01% via ATR trailing stop (held ~3.5d). AUR entered 2026-07-13 at $6.18. Account at $100.94. Log trimmed to 6/15 entries. RL has 19 states learned, Q-table veto active.

## 2026-07-10
- Trades analysed: 3 (RKLB +2.93%, GS -2.46%, SMCI +2.41%; 4 open: WMT/DKNG/JPM/DELL)
- Win rate: 66.7% overall (normal: 66.7% — 2W/1L; momentum: n/a; surge: n/a)
- Config changes: none — RSI_OVERSOLD: n=3 < 5 (need ≥5); MOMENTUM_VOL_MIN: no momentum entries in log; ATR_VOLATILITY_THRESHOLD: avg_hold 31h > 2h, avg_pnl +0.99% > 0
- Backtest: SKIPPED — yfinance proxy blocked (403). Prior metrics retained: +9.29% 365d return, 15.3% drawdown, 39.6% win rate
- RL samples: 366/200 (READY — exceeds target)
- Notes: RL READY for Q-learning activation. DELL position at -5.27%, flagged below stop $440.03 — sell at next market open. Account $101.34. Log trimmed to 9/15 entries.

## 2026-07-16
- Trades analysed: 2 confirmed closed in recent log (DKNG +0.71% ATR trail, held 12d; AUR -4.1% ATR trail, held ~48h)
- Win rate: 50.0% overall (normal: 50.0% — 1W/1L; momentum: n/a — 0 closed; surge: n/a — 0 closed)
- Config changes: none — RSI_OVERSOLD: n=2 < 5 (need ≥5); MOMENTUM_VOL_MIN: no momentum entries (n<3); ATR_VOLATILITY_THRESHOLD: avg_hold ~144h >> 2h threshold, rule not triggered
- Backtest: SKIPPED — yfinance proxy blocked (403). Prior 365d metrics retained: +9.29% return, 15.3% drawdown, 39.6% win rate
- RL samples: 392/200 (READY — +12 new rows today; 19 states in Q-table)
- Notes: 3 open positions: WMT +4.2%, JPM +3.1%, DIS +1.2% (entered today). DIS RSI SELL signal (RSI 71.1) deferred to next market open. Account $100.29. Log trimmed to 12 entries. RL well past 200 target — Q-agent training recommended.

## 2026-07-20
- Trades analysed: 8 closed cumulative (RKLB +2.93%, SMCI +2.41%, GS -2.46%, DELL -6.01%, DKNG +0.71%, AUR -4.10%, WMT +5.28%, DIS -2.28%) + 1 open (JPM +1.84%)
- Win rate: 50.0% overall (normal: 50.0% — 4W/4L, avg_pnl -0.44%, avg_hold 175h; momentum: n/a — 0 trades; surge: n/a — 0 trades)
- Config changes: none — RSI_OVERSOLD: win_rate=50% in 40-65% range, NO_CHANGE; MOMENTUM_VOL_MIN: no momentum closed trades (n<3), NO_CHANGE; ATR_VOLATILITY_THRESHOLD: avg_hold 175h >> 2h threshold, NO_CHANGE
- Backtest: SKIPPED — yfinance proxy blocked (403). Prior 365d metrics retained: +9.29% return, 15.3% drawdown, 39.6% win rate
- RL samples: 392/200 (READY — 0 new rows today; 19 states in Q-table)
- Notes: DIS exited at -2.28% via ATR trailing stop (held 95h). WMT exited at +5.28% via net_buy_signal reversal (held 15d). JPM currently +1.84% @ $339.15, trail $334.69. Account $99.89 (below $100 start). Bearish_EMA regime active. Log trimmed to 3 entries.

## 2026-07-21
- Trades analysed: 8 closed cumulative (same as 2026-07-20; no new exits today) + 1 open (JPM +3.64%)
- Win rate: 50.0% overall (normal: 50.0% — 4W/4L, avg_pnl -0.44%, avg_hold 175h; momentum: n/a — 0 trades; surge: n/a — 0 trades)
- Config changes: none — RSI_OVERSOLD: win_rate=50% in [40%,65%], NO_CHANGE (n=8≥5); MOMENTUM_VOL_MIN: n=0 momentum trades (n<3), NO_CHANGE; ATR_VOLATILITY_THRESHOLD: avg_hold 175h >> 2h, NO_CHANGE
- Backtest: SKIPPED — yfinance proxy blocked (403). Prior 365d metrics retained: +9.29% return, 15.3% drawdown, 39.6% win rate
- RL samples: 395/200 (READY — +3 new rows today; 19 states in Q-table)
- Notes: JPM now +3.64% @ $345.15, trail $334.69, TP $366.32. Regime: normal/BULLISH. All buys blocked today by cash buffer ($84.62 buying power — after JPM position only $34.62 available above $50 buffer). Account $100.17. Peak $101.68. Log trimmed to 7 entries. RL well past 200 — run python -m strategy.rl_agent --train to activate Q-agent.

## 2026-07-24
- Trades analysed: 2 closed in trimmed log (JPM +4.1% BULLISH EMA/signal-sell; PLTR +0.105% BEARISH EMA/signal-sell)
- Win rate: 100% in-log (normal: 100% — 2W/0L; momentum: n/a — 0 trades; surge: n/a — 0 trades) — note: insufficient n for statistical significance
- Config changes: none — RSI_OVERSOLD: n=2 < 5 (need ≥5), NO_CHANGE; MOMENTUM_VOL_MIN: n=0 momentum trades (n<3), NO_CHANGE; ATR_VOLATILITY_THRESHOLD: avg_pnl > 0 (wins), rule not triggered
- Backtest: SKIPPED — yfinance proxy blocked (403). Prior 365d metrics retained: +9.29% return, 15.3% drawdown, 39.6% win rate
- RL samples: 412/200 (READY — +5 new rows today; 19 states in Q-table)
- Notes: Account $100.28, 0 open positions, regime bearish_ema (SPY $738.85 < EMA200 $744.44). Log trimmed to 9/15 entries. RL exceeds 200 target by 212 — Q-agent training recommended.

## 2026-07-27
- Trades analysed: 1 closed in trimmed log (PLTR +0.105% normal/BEARISH EMA/signal-sell — net buy reversed at 25.9h)
- Win rate: 100% in-log (1W/0L) — insufficient n for statistical significance (n<5 normal, n=0 momentum/surge)
- Config changes: none — RSI_OVERSOLD: n=1 < 5 (need ≥5), NO_CHANGE; MOMENTUM_VOL_MIN: n=0 momentum trades (n<3), NO_CHANGE; ATR_VOLATILITY_THRESHOLD: avg_hold 25.9h > 2h threshold and avg_pnl > 0, rule not triggered
- Backtest: SKIPPED — yfinance proxy blocked (403). Prior 365d metrics retained: +9.29% return, 15.3% drawdown, 39.6% win rate
- RL samples: 415/200 (READY — +3 new rows today; 19 states in Q-table)
- Notes: Account $101.58, 1 open position (AMD +2.6% @ $495.07, trail $484.89, TP $530.73), regime bearish_ema. RL well past 200 target — run python -m strategy.rl_agent --train to activate Q-agent. Log trimmed to 6 entries.

## 2026-07-28
- Trades analysed: 1 closed (AMD -5.96% stop, 21.1h hold, normal/BEARISH)
- Win rate: 0% overall (normal: 0% n=1, momentum: n/a n=0, surge: n/a n=0)
- Config changes: none — all types below minimum sample thresholds (normal n<5, momentum n<3, ATR hold not <2h)
- Backtest: SKIPPED — yfinance proxy blocked (403), prior metrics retained (return +9.3%, drawdown 15.3%, win_rate 39.6%)
- RL samples: 417/200 — READY (exceeded target by 217)
- Notes: bearish_ema regime active all day (SPY $741.45 < EMA200 $743.93); no new positions opened (buying power at buffer limit $50.28); AMD position closed by ATR trailing stop at -6.0% from avg; account at $97.45 (-2.8% weekly from $100.28 start)

## 2026-07-30
- Trades analysed: 11 total closed (normal: 6W/5L; momentum: n/a n=0; surge: n/a n=0)
- Win rate: 54.5% overall (normal: 54.5% — 6W/5L, avg_pnl −0.48%, avg_hold ~153h; momentum: n/a; surge: n/a)
- EMA-trend win rate: BULLISH entry 55.6% (5W/4L, n=9); BEARISH entry 50.0% (1W/1L, n=2)
- Config changes: none — RSI_OVERSOLD: win_rate=54.5% in [40%,65%] range, NO_CHANGE (n=11≥5); MOMENTUM_VOL_MIN: n=0 momentum trades (n<3), NO_CHANGE; ATR_VOLATILITY_THRESHOLD: avg_hold ~153h >> 2h, NO_CHANGE
- Backtest: SKIPPED — yfinance proxy blocked (403); prior 365d metrics retained (+9.29% return, 15.29% drawdown, 39.6% win rate)
- RL samples: 419/200 (READY — +1 new row today; 19 states in Q-table)
- Notes: Account $97.45 cash-only (−2.8% week from $100.28), regime bearish_ema (SPY below EMA200 all day). No positions. Multiple signals blocked by bearish_ema 3/3 conf rule + cash buffer bind. RL exceeds 200 target by 219 — run `python -m strategy.rl_agent --train`. Trade log trimmed to 9 entries.

## 2026-07-29
- Trades analysed: 1 (AMD only — normal/BEARISH EMA, -6.0% stop, ~21h hold)
- Win rate: 0% overall (normal: 0% [n=1], momentum: n/a [n=0], surge: n/a [n=0])
- Config changes: none (all strategy types below minimum n thresholds — normal n<5, momentum n<3, surge n<3)
- Backtest: skipped — yfinance proxy blocked (403); prior metrics retained (return +9.29%, drawdown 15.29%, win_rate 39.6%)
- RL samples: 418/200 (READY — RL training can be activated)
- Notes: Account $97.45 cash-only, regime bearish_ema, no open positions. Multiple RL BOOST signals blocked by cash buffer constraint ($97.45 − $50 = $47.45 < $50 buffer required). RL fully ready (418 samples, 19 states); consider running `python -m strategy.rl_agent --train` to activate Q-learning. Trade log trimmed to 7 entries.

## 2026-07-31
- Trades analysed: 0 closed pairs (only 2 BUYs placed today: AAPL + MSFT — both still open). No completed trade history to analyze.
- Win rate: n/a — no closed trades in log (normal: n/a, momentum: n/a, surge: n/a)
- Config changes: none — 0 closed trade pairs (n < 3 for all strategy types); NO_CHANGE warranted
- Backtest: SKIPPED — yfinance proxy blocked (403 again). Prior metrics retained: +9.29% return, 15.3% drawdown, 39.6% win rate, 227 trades
- RL samples: 423/200 (READY — +4 new rows today; 19 states in Q-table)
- Notes: Live account $98.18. Positions: AAPL +2.35% (entry $301.95, trail_stop $291.73), MSFT open (entry $462.02). Regime shifted bearish_ema → normal today (SPY $745.44 > EMA200 $743.41). RL exceeded 200 target days ago — Q-table has 19 states. Trade log trimmed to 12 entries (last 2 days). Run: python -m strategy.rl_agent --train to activate Q-learning.
