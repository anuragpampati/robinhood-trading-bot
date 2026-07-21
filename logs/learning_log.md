# Learning Log — Robinhood Agentic Account

> Auto-maintained by daily learning CCR agent.

---

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
