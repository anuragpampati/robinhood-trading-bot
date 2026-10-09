# Trade Log — Robinhood Agentic Account

## 2026-10-09T20:12:09Z
- SUMMARY: Market closed. Buying power: $50.00. Equity positions: 1 (AMKR @ $49.14, trail=$48.38, pnl=-0.41%). Regime: normal. Account: $243.79 (broker). Universe fetched: 503. No trades. CB: daily +0.31%/weekly -1.31% (OK). Kill switch: OK (trading_enabled=true).

## 2026-10-09T18:12:00Z
- SUMMARY: Market open, in_trade_window=true. No trades. BP=$50 (investable=$0). No SELL: AMKR HOLD ($48.93, trail=$48.38 OK, ~4h held, pnl=-0.83%, rsi=24.79 BUY conf=2, rl=HOLD/0.93). 3 RSI BUY signals (ON conf=2/AMKR already held/CTVA conf=2) SKIPPED investable=$0. 0 net-buy BUYs. Surge: ANET 3.9% (<10%). HUM removed from surge tracker. CB: daily -0.49%/weekly -2.09% (OK). Regime=normal. Acct=$241.86. Universe=503.

## 2026-10-09T17:20:00Z
- SUMMARY: Market open, in_trade_window=true. No trades. BP=$50.00 (investable=$0). No SELL conditions: AMKR HOLD ($49.25, trail=$48.38 OK, ~3h held, pnl=-0.18%, no exit triggers). 1 RSI BUY (IREN conf=2, rl=HOLD/0.93, SKIPPED investable=$0). 0 net-buy BUYs. HUM surge count=2 (≥10%, INTRADAY_SURGE threshold reached) but SELL signal (rsi=73.8) + $0 investable — no buy. CB: daily -0.07%/weekly -1.69% (OK). Regime=normal. Acct=$242.86. Universe=503.

## 2026-10-09T16:14:06Z
- SUMMARY: Market open, in_trade_window=true. No trades. BP=$50.00 (investable=$0). No SELL conditions: AMKR HOLD ($49.40, trail=$48.38 OK, ~2h held, pnl=+0.12%). 0 RSI BUYs, 0 net-buy BUYs. Surge: HUM 14.6% (first sighting today, count=1, need 2 for INTRADAY_SURGE; no tracker buy). CB: daily +0.15%/weekly -1.47% (OK, no trip). Regime=normal. Acct=$243.40. Universe=503.

## 2026-10-08T19:12:00Z
- SUMMARY: Market open, in_trade_window=true. No trades. BP=$50.00 (investable=$0). No SELL conditions: MOS HOLD ($19.85, trail=$19.69 OK, rsi=28.26 low-vol skip, rl=BUY 0.928, ~27h held, pnl=-0.95%). 0 RSI BUYs, 1 net-buy BUY (ACN conf=MODERATE) SKIPPED: investable=$0. 3 surge signals (ACN/CINF/EOG all 0% surge, none ≥10%). Surge tracker cleared (XOM/DG/DOW removed, all <10%). CB: daily -1.11%/weekly -1.48% (OK). Regime=normal. Acct=$243.37. Universe=503.

## 2026-10-08T18:12:58Z
- Action   : SELL SOUN
- Price    : $5.4635 (fill) | Entry: $5.5785
- Amount   : $125.39 | Shares: 22.939858
- RSI      : 20.78 (BUY signal, but selling) | EMA: BEARISH | BB: BELOW_BAND
- RL       : HOLD conf=0.936 | null (no veto/boost)
- Stop     : $5.47 (ATR trail) | Target was: $6.14
- Strategy : normal | Sell: ATR trail stop triggered ($5.4671 ≤ $5.47)
- Regime   : normal
- Reason   : ATR trailing stop hit (-2.06% loss, $5.4635 vs avg_cost $5.5785). Hours held ~4h ≥ 3h threshold met. Buying power $50 (investable $0) — no new BUYs. 18 RSI BUY signals (all conf=2, all HOLD by RL), 0 net-buy BUYs. Surge first sightings: XOM/DG/DOW (count=1, need 2). CB: daily -1.11%/weekly -1.48% (OK). Regime=normal. Acct=$243.37. Universe=503.

## 2026-10-08T17:11:51Z
- SUMMARY: Market open (ET ~13:12). No trades. 0 RSI BUY signals, 0 net-buy BUY signals, 0 surge signals. No SELL conditions triggered. 2 positions: MOS HOLD ($19.945, trail=$19.69 OK, >24h held, -0.47%), SOUN HOLD ($5.505, trail=$5.47 OK, ~3h held, -1.34%). Buying power: $50.00. CB: daily -0.80%/weekly -1.18% (OK). Regime=normal. Acct=$244.11. Universe=503.

## 2026-10-08T15:15:00Z
- SUMMARY: Market open (ET ~11:14). No trades. Buying power $50.00 = cash buffer → investable=$0, no new BUYs possible. 26 RSI BUY signals (best: INTC/QCOM/ARM conf=2+RL BOOST→3, GRMN rsi=17.79). No SELL conditions triggered on held positions. 2 positions: MOS $20.005 +0.00% (trail=$19.69 OK), SOUN $5.57 -0.18% (trail=$5.47, <3h hold). Surge tracker: CEG removed (not in >=10% surge signals any more). CB: daily -0.15%/weekly -0.53% (OK). Regime=normal. Acct=$245.73. Universe=503.

## 2026-10-08T14:13:42Z
- Action   : BUY SOUN
- Price    : $5.58
- Amount   : $127.97 | Shares: 22.9337
- RSI      : 29.92 | EMA: BEARISH | BB: BELOW_BAND
- RL       : BUY conf=0.928 | BOOST (conf 2→3 STRONG BUY)
- Stop     : $5.47 | Target: $6.14
- Strategy : normal | Sell date: ATR/signal
- Regime   : normal
- Reason   : RSI oversold+stabilizing (28.7→29.9) | BB reversal returning from band | RL BOOST STRONG BUY | investable=$127.97

## 2026-10-08T14:13:25Z
- Action   : SELL MRK
- Price    : $140.64
- Amount   : $19.30 | Shares: 0.137271
- RSI      : n/a | EMA: n/a | BB: n/a
- RL       : n/a
- Stop     : ATR trail $140.86 triggered | Target: $154.18
- Strategy : normal | Sell date: ATR trail stop
- Regime   : normal
- Reason   : ATR trail stop triggered ($140.64 ≤ $140.86, held ~48h). Entry=$140.16. PnL: +0.34% (+$0.07)

## 2026-10-08T14:13:22Z
- Action   : SELL ERIE
- Price    : $218.45
- Amount   : $32.37 | Shares: 0.148186
- RSI      : n/a | EMA: n/a | BB: n/a
- RL       : n/a
- Stop     : ATR trail $220.97 triggered | Target: $245.93
- Strategy : normal | Sell date: ATR trail stop
- Regime   : normal
- Reason   : ATR trail stop triggered ($218.45 ≤ $220.97, held ~24h). Entry=$223.57. PnL: -2.29% (-$0.76)

## 2026-10-08T14:13:00Z
- SUMMARY: Market OPEN (ET ~10:13). Sold ERIE (ATR trail) and MRK (ATR trail). Bought SOUN $127.97 (RSI conf=2 + RL BOOST → conf=3 STRONG BUY). Regime=normal. Acct≈$246.09. BP≈$50 (post-buy, ERIE+MRK proceeds unsettled). 2 positions: MOS, SOUN. CB: daily=0%/weekly=-0.38% (new day, OK). Universe=503. USB skipped (STRONG BUY but no investable after SOUN). CEG surge count=1 (not yet 2, no buy).

## 2026-10-07T19:15:46Z [BACKFILL — prior cycle, not previously logged]
- Action   : SELL VTR
- Price    : $80.44
- Amount   : $18.88 | Shares: 0.234720
- RSI      : ~21.1 (oversold, HOLD) | EMA: BEARISH | BB: N/A
- RL       : null conf=null | null
- Stop     : $80.66 (ATR trail) triggered — price $80.44 ≤ $80.66
- Target   : $90.17 (+10%) — not reached
- Strategy : normal | Sell trigger: ATR trailing stop
- Regime   : normal
- Reason   : ATR trail stop hit: $80.44 ≤ $80.66; hours_held ~24h; PnL -1.87% from avg_cost $81.97. Exit per rule.

## 2026-10-07T19:08:28Z [BACKFILL — prior cycle, not previously logged]
- Action   : SELL GE
- Price    : $304.12
- Amount   : $38.02 | Shares: 0.125087
- RSI      : ~29.2 (near-oversold, HOLD) | EMA: BULLISH | BB: N/A
- RL       : null conf=null | null
- Stop     : $303.90 (ATR trail) triggered — price $304.12 ≥ $303.90 (price was near stop)
- Target   : $338.39 (+10%) — not reached
- Strategy : normal | Sell trigger: ATR trailing stop
- Regime   : normal
- Reason   : ATR trail stop triggered; hours_held ~29h; PnL -1.14% from avg_cost $307.63. Exit per rule.

## 2026-10-07T19:15:46Z [BACKFILL — prior cycle, not previously logged]
- Action   : SELL VTR
- Price    : $80.44
- Amount   : $18.88 | Shares: 0.234720
- RSI      : ~21.1 (oversold, HOLD) | EMA: BEARISH | BB: N/A
- RL       : null conf=null | null
- Stop     : $80.66 (ATR trail) triggered — price $80.44 ≤ $80.66
- Target   : $90.17 (+10%) — not reached
- Strategy : normal | Sell trigger: ATR trailing stop
- Regime   : normal
- Reason   : ATR trail stop hit: $80.44 ≤ $80.66; hours_held ~24h; PnL -1.87% from avg_cost $81.97. Exit per rule.

## 2026-10-07T19:08:28Z [BACKFILL — prior cycle, not previously logged]
- Action   : SELL GE
- Price    : $304.12
- Amount   : $38.02 | Shares: 0.125087
- RSI      : ~29.2 (near-oversold, HOLD) | EMA: BULLISH | BB: N/A
- RL       : null conf=null | null
- Stop     : $303.90 (ATR trail) triggered — price $304.12 ≥ $303.90 (price was near stop)
- Target   : $338.39 (+10%) — not reached
- Strategy : normal | Sell trigger: ATR trailing stop
- Regime   : normal
- Reason   : ATR trail stop triggered; hours_held ~29h; PnL -1.14% from avg_cost $307.63. Exit per rule.
