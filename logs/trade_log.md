# Trade Log — Robinhood Agentic Account

## 2026-09-11T16:13:20Z
- SUMMARY: Market OPEN (~12:13 PM ET). Regime: normal (SPY $765.73 > EMA200 $762.70). RSI BUY: 0 | Net Buy BUY: 0. MRNA surge 18.9% → tracker count=1 (need ≥2 for intraday_surge buy; surge ≥5% buy also blocked: $98.49 − $50 = $48.49 < $50 buffer). TXN RSI SELL (72.6, conf 2/3) — not held. Net-buy SELL signals: NVDA/UBER/JPM/BAC/AAPL/WFC/PFE/PYPL/F/ROK — none held. 0 positions to sell. CB INACTIVE (daily 0.0%, weekly gain +1.13%). BP $98.49. 0 positions. Acct $98.49.

## 2026-09-10T19:09:00Z
- SUMMARY: Market OPEN (~3:09 PM ET). PANIC regime (SPY RSI 27.1 < 30) + bearish_ema — all individual stock buys suppressed. 0 positions held — nothing to sell. No surge/intraday_surge signals. Deployable $14.99 (BP $64.99 − $50 buffer) below $15 min order. Net-buy SELL: JPM/KTOS/WMT/GE/MRCY/MSFT/AI/SBUX/CRWD/SPY/SNAP/C/NOW — none held. CB INACTIVE (daily −0.43%, weekly gain +1.13%). BP $64.99. 0 positions. Acct $98.49.

## 2026-09-10T18:10:34Z
- Action   : SELL SBUX
- Price    : $99.67
- Amount   : $33.52 | Shares: 0.336408
- RSI      : 25.6 | EMA: BEARISH | BB: IN_BAND
- RL       : null conf=null | null
- Stop     : $99.61 | Target: $111.14
- Strategy : normal | Sell date: ATR/signal
- Regime   : bearish_ema
- Reason   : Net buy reversal (SBUX -0.69M→-0.83M, OBV ↓) | hours_held ~24h ≥ 3h | trail_stop $99.61 near breach | PnL ≈ -1.4%

## 2026-09-10T16:12:35Z
- SUMMARY: Market OPEN (~12:12 ET). PANIC regime (SPY RSI 26.7 < 30) + bearish_ema — all individual stock buys suppressed. No RSI BUY signals. Surge tracker cleared (MRVL/ARM no longer in 10%+ surge signals). Deployable $14.99 (below $15 min order). RSI SELL: QCOM (RSI 73.1) — not held. Net-buy SELL: WMT/GE/MRCY/GOOGL/KTOS/AI/JPM — none held. SBUX held: $99.97 vs stop $99.61 / target $111.14 — no exit. CB INACTIVE (daily -0.28%, weekly +1.28% gain). BP $64.99. 1 position. Acct $98.64.

## 2026-09-09T19:12:30Z
- SUMMARY: Market OPEN (15:12 ET). Bearish_ema regime — 3/3 confidence required. RSI BUY candidates: IWM (RSI 27.2, conf 2→3 RL BOOST, but net_buy SELL conflict + $0 headroom after $50 buffer), UBER (RSI 28.0, conf 2/3, HOLD RL), SHOP (RSI 21.2, conf 2/3, HOLD RL) — none qualify. Net-buy SELL signals: CRM/MBLY/NFLX/SHOP/F/AVAV/MSFT/IWM/UBER — none held. SBUX held: $100.62 vs stop $99.61 / target $111.14 — no exit triggered (held <3h, price above stop). Surge tracker cleared (ORCL expired). CB INACTIVE (daily -0.09%, weekly +1.5% gain). Buying power: $50.00 (at buffer minimum). Equity positions: 1 (SBUX). Regime: bearish_ema. Account: $98.84.

## 2026-09-09T15:12:49Z
- Action   : SELL NFLX
- Price    : $76.59
- Amount   : $14.95 | Shares: 0.195238
- RSI      : 25.5 | EMA: BEARISH | BB: IN_BAND
- RL       : BUY conf=0.928 | null
- Stop     : $75.40 | Target: $84.51
- Strategy : normal | Sell date: ATR/signal
- Regime   : normal
- Reason   : Net buy trend reversed (5.01M → 0.01M | OBV -5.7M/day) | held 21h → rule c (signal SELL)
