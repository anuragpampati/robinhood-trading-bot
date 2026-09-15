# Trade Log — Robinhood Agentic Account

## 2026-09-15T15:14:00Z
- SUMMARY: Market OPEN, in trade window. Signal engine data-blocked (yfinance proxy restrictions — 0/103 tickers fetched). No actionable signals. No trades placed. NVDA held: $212.24, −0.08% (above trail stop $209.19). Circuit breaker INACTIVE (daily 0.03%, weekly 0.66%). Buying power: $148.49 (settled; $221.86 cash, ~$73 unsettled from SBUX+UUUU sells). Equity positions: 1. Regime: normal (signal engine; prior cycle: bearish_ema). Account: $246.84.

## 2026-09-15T14:12:31Z
- Action   : SELL SBUX
- Price    : $97.35
- Amount   : $49.14 | Shares: 0.504874
- RSI      : N/A (yfinance proxy-blocked this cycle) | EMA: N/A | BB: N/A
- RL       : null conf=null | null
- Stop     : $97.85 ATR trail_stop hit | Target was: $108.93
- Strategy : normal | Sell date: ATR trail stop triggered
- Regime   : bearish_ema (last known; signal engine unreliable — no market data)
- Reason   : ATR trailing stop: price $97.35 ≤ trail_stop $97.85 | held ~24h | loss −1.70%

## 2026-09-15T14:12:25Z
- Action   : SELL UUUU
- Price    : $12.09
- Amount   : $24.29 | Shares: 2.008048
- RSI      : N/A (yfinance proxy-blocked this cycle) | EMA: N/A | BB: N/A
- RL       : null conf=null | null
- Stop     : $12.09 ATR trail_stop hit | Target was: $13.695
- Strategy : normal | Sell date: ATR trail stop triggered
- Regime   : bearish_ema (last known; signal engine unreliable — no market data)
- Reason   : ATR trailing stop: price $12.09 ≤ trail_stop $12.09 | held ~24h | loss −2.89%

## 2026-09-15T14:13:00Z
- SUMMARY: Market OPEN, in_trade_window=true. Signal engine: 0 RSI BUY, 0 net-buy, 0 surge — Yahoo Finance proxy-blocked, all 103 tickers failed yfinance download; regime defaulted to "normal" (unreliable). No new BUY orders. SOLD SBUX (ATR stop $97.35≤$97.85, −1.70%) and UUUU (ATR stop $12.09≤$12.09, −2.89%). NVDA HELD: $212.46 > trail_stop $209.19. CB INACTIVE (daily 0.00%, weekly 0.63%). BP ~$221.93 (est post-sell). 1 position. Acct ~$246.94.

## 2026-09-14T19:12:10Z
- Action   : BUY NVDA
- Price    : $212.42
- Amount   : $25.00 | Shares: 0.117690
- RSI      : 27.87 | EMA: BEARISH | BB: BELOW_BAND
- RL       : BUY conf=0.952 | BOOST (conf 2→3)
- Stop     : $209.19 | Target: $233.66
- Strategy : normal | Sell date: ATR/signal
- Regime   : bearish_ema
- Reason   : RSI 27.87 deeply oversold | BB below lower band | RL BOOST conf 2→3 | bearish_ema $25 cap

## 2026-09-14T18:11:00Z
- SUMMARY: Market OPEN (~2:11 PM ET). Regime: bearish_ema (SPY $762.35 below EMA200 $763.33 — max $25/pos, 3/3 conf required). RSI BUY: 0. Net Buy BUY: 0. Surge: 0 (MSFT surge count=1 expired — no longer in 10%+ surge list). No trades placed. CB INACTIVE (daily −0.11%, weekly −0.11%). Holdings: SBUX 0.5049sh @ $98.905 (−0.13%, stop $97.85, held ~4h); UUUU 2.0080sh @ $12.345 (−0.84%, stop $12.09, held ~4h). No exit triggers fired. BP $173.49. 2 positions. Acct $248.21.

## 2026-09-14T16:11:10Z
- SUMMARY: Market OPEN (~12:11 PM ET). Regime: bearish_ema (SPY below EMA200 — max $25/pos, 3/3 conf required). RSI BUY: 0. Net Buy BUY: 0. Surge: 0. No trades placed. CB INACTIVE (daily −0.24%, weekly −0.24%). Holdings: SBUX 0.5049sh @ $98.44 (−0.60%, stop $97.85, held ~2h, exits gated until 17:12 UTC); UUUU 2.0080sh @ $12.305 (−1.17%, stop $12.09, held ~2h, exits gated). BP $173.49. 2 positions. Acct $247.90.

## 2026-09-14T15:11:26Z
- SUMMARY: Market OPEN (~11:11 AM ET). Regime: bearish_ema (SPY $758.57 < EMA200 $763.39 — max $25/pos, 3/3 conf required). RSI BUY: 0 candidates. Net Buy BUY: 0. Surge: none. No trades placed. CB INACTIVE (daily −0.21%, weekly −0.21%). Holdings: SBUX 0.5049sh @ $98.39 (−0.65%, stop $97.85); UUUU 2.0080sh @ $12.30 (−1.24%, stop $12.09). Both held <3h — ATR/signal exits gated until 17:12 UTC. BP $173.49. 2 positions. Acct $247.98.

## 2026-09-14T14:11:51Z
- Action   : BUY UUUU
- Price    : $12.45
- Amount   : $25.00 | Shares: 2.008030
- RSI      : 20.94 | EMA: BEARISH | BB: BELOW_BAND
- RL       : HOLD conf=0.93 | null
- Stop     : $12.09 | Target: $13.70
- Strategy : normal | Sell date: ATR/signal
- Regime   : normal
- Reason   : RSI oversold+stabilizing (22.8≈20.9) | BB reversal: 0.11→0.13 (returning from band)

## 2026-09-14T14:11:46Z
- Action   : BUY SBUX
- Price    : $99.04
- Amount   : $50.00 | Shares: 0.504840
- RSI      : 26.75 | EMA: BEARISH | BB: BELOW_BAND
- RL       : BUY conf=0.928 | BOOST (conf 2→3)
- Stop     : $97.85 | Target: $108.94
- Strategy : normal | Sell date: ATR/signal
- Regime   : normal
- Reason   : RSI oversold+stabilizing (28.5≈26.7) | BB reversal: 0.17→0.20 (returning from band) | RL BOOST

## 2026-09-13 16:13:30
- Market closed — no trades placed.
