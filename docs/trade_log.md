# Trade Log — Robinhood Agentic Account

## 2026-09-29T16:12:00Z
- SUMMARY: Market OPEN, in_trade_window=true. Regime=bearish_ema (SPY BEARISH below 200-EMA). No SELLs: all 4 ATR stops safe (PNR $52.99>$52.19 ✓, INVH $26.46>$26.02 ✓, VICI $23.175>$23.00 ✓, CRM $227.56>$226.51 ✓; no SELL signals for held tickers). No BUYs: 0 RSI BUY signals, 0 net_buy_buy signals, 0 surge signals (bearish_ema regime — all buys halted without 3/3 confidence). CB: daily 0.0%/weekly 0.5% (OK). 4 positions (PNR:-0.4%@$52.99, INVH:+0.6%@$26.46, VICI:-0.4%@$23.175, CRM:-0.6%@$227.56). Universe=503. BP=$114.44. Acct=$244.23.

## 2026-09-29T15:31:33Z
- Action   : SELL REGN
- Price    : $745.58
- Amount   : $18.09 | Shares: 0.024261
- RSI      : 23.1 | EMA: BEARISH | BB: BELOW_BAND
- RL       : HOLD conf=0.93 | null
- Stop     : $753.28 (triggered) | Target: $838.34
- Strategy : normal | Sell date: ATR trailing stop
- Regime   : normal
- Reason   : ATR trailing stop triggered: $745.58 ≤ trail_stop $753.28 (entry $762.13, loss -2.19%)

## 2026-09-29T15:31:00Z
- SUMMARY: Market OPEN, in_trade_window=true. SOLD REGN (ATR trail stop $753.28 triggered, current $745.58, entry $762.13, loss -2.19%). CDW RSI BUY conf=2 (RSI=23.3) SKIPPED: in net_buy_sell + EMA BEARISH + RL HOLD@93% — too many contradicting signals, HOLD. CB: daily 0.0%/weekly 0.50% (OK). Regime=normal. Universe=503. 4 positions (PNR:-0.7%@$52.79, INVH:+0.8%@$26.53, VICI:-0.5%@$23.15, CRM:-0.6%@$227.55). BP=$114.44. Acct=$244.22.

## 2026-09-28T20:15:00Z
- SUMMARY: Market CLOSED (after 4pm ET). Regime=normal (SPY BULLISH above 200-EMA). No SELLs (market closed — skipped). No BUYs (market closed + 5/5 max positions). ATR stops vs close: PNR $53.04>$52.19 ✓, INVH $26.55>$26.02 ✓, VICI $23.20>$23.00 ✓, CRM $227.27>$226.51 ✓, REGN $752.42<$753.28 ⚠ BELOW STOP. REGN ATR trail stop will trigger SELL at next market open (hours_held≥3 since 2026-09-28T14:19Z). No ratchet updates (all positions at/below cost). CB: daily 0.40%/weekly 0.40% (OK, under 3%/5%). Surge: WAT count=2 (≥10% threshold, held from last cycle — mkt closed, tracker unchanged). RSI/Net-buy: all 5 held = HOLD. Universe=503. BP=$68.48. Acct=$244.45.

## 2026-09-28T18:13:00Z
- SUMMARY: Market OPEN, in_trade_window=true. Regime=normal (SPY BULLISH above 200-EMA). No SELLs (all 5 ATR stops safe: PNR $53.23>$52.19, INVH $26.54>$26.02, VICI $23.29>$23.00, CRM $228.85>$226.51, REGN $754.11>$753.28; no SELL signals for any held positions). No BUYs (5/5 max positions). CB: daily 0.20%/weekly 0.20% (OK). RSI BUY candidates skipped (max positions): CRM(conf2,RL-BUY→3), TSLA(conf2,RL-BUY→3), NFLX(conf2,RL-BUY→3), REGN(conf2,RL-HOLD), +16 more. Surge: WAT 33.9% count=1 (need 2). Universe=503. 5 positions (PNR:+0.09%@$53.23, INVH:+0.86%@$26.54, VICI:+0.11%@$23.29, CRM:-0.08%@$228.85, REGN:-1.05%@$754.11). BP=$68.48. Acct=$244.94.

## 2026-09-28T14:20:00Z
- SUMMARY: Market OPEN, in_trade_window=true. Regime=normal (SPY BULLISH above 200-EMA). Universe=503 (RH historicals cache, 502 symbols fetched). SELLs: CTSH (ATR stop $56.38≤$56.49), FFIV (ATR stop $436.38≤$438.20). BUYs: CRM $36.97 (RL BOOST RSI=25.23), REGN $18.49 (RL BOOST RSI=26.18). CB: daily 0.0%/weekly 0.0% (new day+week start). 5 positions (PNR/INVH/VICI/CRM/REGN). BP=$68.48. Acct=$245.44.

## 2026-09-28T14:19:18Z
- Action   : BUY REGN
- Price    : $762.13
- Amount   : $18.49 | Shares: 0.024261
- RSI      : 26.18 | EMA: BEARISH | BB: BELOW_BAND
- RL       : BUY conf=0.928 | RL BOOST (conf 2→3)
- Stop     : $753.28 | Target: $838.34
- Strategy : normal | Sell date: ATR/signal
- Regime   : normal
- Reason   : RSI oversold+stabilizing (26.2→26.2) | BB reversal: 0.10→0.15 (returning from band) | RL BOOST

## 2026-09-28T14:18:58Z
- Action   : BUY CRM
- Price    : $229.03
- Amount   : $36.97 | Shares: 0.161418
- RSI      : 25.23 | EMA: BEARISH | BB: BELOW_BAND
- RL       : BUY conf=0.928 | RL BOOST (conf 2→3)
- Stop     : $226.51 | Target: $251.93
- Strategy : normal | Sell date: ATR/signal
- Regime   : normal
- Reason   : RSI oversold+stabilizing (25.2→25.2) | BB reversal: 0.12→0.16 (returning from band) | RL BOOST

## 2026-09-28T14:18:04Z
- Action   : SELL FFIV
- Price    : $436.38
- Amount   : $21.54 | Shares: 0.049355
- RSI      : n/a | EMA: n/a | BB: n/a
- RL       : null conf=null | null
- Stop     : ATR trail stop hit ($436.38 ≤ $438.20) | Entry: $447.98
- Strategy : normal | PnL: -2.59%
- Regime   : normal
- Reason   : ATR trailing stop triggered (current $436.38 ≤ trail_stop $438.20, held ~71h)

## 2026-09-28T14:17:56Z
- Action   : SELL CTSH
- Price    : $56.38
- Amount   : $24.50 | Shares: 0.434405
- RSI      : n/a | EMA: n/a | BB: n/a
- RL       : null conf=null | null
- Stop     : ATR trail stop hit ($56.38 ≤ $56.49) | Entry: $57.55
- Strategy : normal | PnL: -2.03%
- Regime   : normal
- Reason   : ATR trailing stop triggered (current $56.38 ≤ trail_stop $56.49, held ~72h)

## 2026-09-28T17:12:28Z
- SUMMARY: Market OPEN, in_trade_window=true. No SELLs (all 5 positions above ATR stops; all signals HOLD; no TP hit). No BUYs (5/5 max positions). Regime=normal. CB: daily 0.29%/weekly 0.29% (OK). RSI BUY candidates skipped (max positions): AMD(conf2), ALAB(conf2), STZ(conf2), CPRT(conf2), EFX(conf2). Surge: XOM 11.8% count=1 (need 2). Universe=503. 5 positions (PNR:-0.50%@$52.92, INVH:+0.49%@$26.44, VICI:-0.06%@$23.25, CRM:-0.02%@$228.98, REGN:-0.85%@$755.66). BP=$68.48. Acct=$244.72.
