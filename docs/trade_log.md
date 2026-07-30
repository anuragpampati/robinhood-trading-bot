# Trade Log — Robinhood Agentic Account

## 2026-07-30T14:17:54.849414+00:00
- SUMMARY: Market open (10:17 ET). No new positions. Buying power: $97.45. 0 equity positions. Regime: bearish_ema (SPY $729.54 < EMA200 $743.42). Account: $97.45. CB: INACTIVE | daily 0.0% | weekly 2.8% (week_start $100.28). SNOW NET-BUY signal (4d streak, 52.7% buy surge) BLOCKED: $97.45−$50=$47.45 < $50 buffer. Surge tracker SNOW count=1 (need ≥2). Peak: $101.68. No sells — 0 positions.

> Auto-maintained by Claude agent. One entry per trade action.

---

## 2026-07-29T18:14:02Z
- SUMMARY: Market open (14:14 ET). No trades executed. Buying power: $97.45. Equity positions: 0. Regime: bearish_ema. Account: $97.45.
- No positions to sell.
- RSI BUY signals: ARM conf=2 (🤖 RL BOOST→3 but net-buy SELL conflicts → SKIP), LRCX conf=2 (🤖 RL BOOST→3, $97.45−$50=$47.45 < $50 buffer → SKIP), LAZR conf=2 (🤖 RL BOOST→3, same buffer issue → SKIP). All buys blocked.
- SNOW: net-buy BUY (11.7% buy surge, 4d streak) + RSI SELL (RSI 70.7, ABOVE_BAND) → conflicting signals → SKIP. Surge tracker: SNOW added count=1.
- Net-buy SELLs (no pos): CRDO, RGTI, ARM, NVTS, IREN, MRVL, MU, VRT, ASTS, RDW. RSI SELLs (no pos): AAPL (77.7), TGT (73.8), NOW (73.8), SNOW (70.7).
- CB: INACTIVE | daily 0.0% (day_start $97.45) | weekly −2.8% (week_start $100.28). Peak: $101.68.
- Regime: bearish_ema (SPY $736.41 < EMA200 $743.56). Requires 3/3 conf + $50 position ≤ available above buffer.

## 2026-07-29T15:15:27Z
- SUMMARY: Market open (11:15 ET). No trades executed. Buying power: $97.45. Equity positions: 0. Regime: bearish_ema. Account: $97.45.
- No positions to sell.
- No BUY signals in any strategy (0 net-buy-buy, 0 RSI-buy, 0 surge). 44 SELL signals — none held.
- RSI SELLs (not held): CRM (RSI 74.2), DIS (71.5), TGT (74.9), F (81.4), GM (75.1), PYPL (70.2), NOW (73.6).
- Net-buy SELLs (not held): AMD, IREN, NVTS, MRVL, LAZR, BE, CRWV, EOSE, CIFR, AMZN + 34 more.
- Surge tracker: DKNG removed (no longer ≥10% surge). Tracker empty.
- CB: INACTIVE | daily 0.0% (day_start $97.45) | weekly −2.8% (week_start $100.28). Peak: $101.68.
- Regime: bearish_ema (SPY $734.82 < EMA200 $743.82). Would require 3/3 conf for any buy.

## 2026-07-29T14:17:42Z
- SUMMARY: Market open (10:17 ET). No trades executed. Buying power: $97.45. Equity positions: 0. Regime: bearish_ema. Account: $97.45.
- No positions to sell.
- BUY candidates (post RL BOOST): AMD conf=2→3 (🤖 RL BOOST, rl_conf=1.00), AMAT conf=2→3 (🤖 RL BOOST, rl_conf=1.00). Amount $50 each (bearish_ema). BLOCKED: $97.45 − $50 = $47.45 < $50 cash buffer. Skipping all buys.
- SURGE: DKNG +100.7% intraday surge — count=1 (need ≥2 for entry).
- Net-buy SELL signals (no pos): XOM, ALAB, AVGO, IREN, TSLA, UBER, LRCX. RSI SELL (no pos): BA, GM.
- CB: INACTIVE | daily 0.0% | weekly −2.8% (week_start $100.28). Peak: $101.68.

## 2026-07-28T19:13:06Z
- SUMMARY: Market open (15:13 ET). No trades executed. Buying power: $50.28. Equity positions: 0. Regime: bearish_ema. Account: $97.45.
- No positions to sell. RSI SELL (no pos): CRM, BA, GM. Net-buy SELL (no pos): IREN, TSLA, ALAB, AVGO, VRT, UBER.
- BUY blocked: $50.28 buying power − $50 buffer = $0.28 available, below $15 min. 0 buy signals (bearish_ema requires 3/3 conf, no qualifying signals).
- Surge: BAC added to tracker (count=1, +106.7% buy surge). CRM removed (below 10% threshold). Needs count≥2 to trigger intraday buy.
- CB: INACTIVE | daily +1.1% gain (day_start $96.38) | weekly −2.8% (week_start $100.28). Peak: $101.68.
- Regime: bearish_ema (SPY $741.45 < EMA200 $743.93). Positions: 0.

---

## 2026-07-28T16:17:00Z
- SUMMARY: Market open (12:17 ET). No trades executed. Buying power: $50.28. Equity positions: 0. Regime: bearish_ema. Account: $97.45.
- ASML: RSI BUY conf=2/3 — skipped: bearish_ema requires 3/3 AND RL=HOLD (conf=0.919).
- No net-buy BUY signals. 7 net-buy SELL + 10 RSI SELL — none held.
- CB: INACTIVE | daily +1.1% | weekly -2.8%. Peak: $101.68.

---

## 2026-07-28T15:20:33Z
- Action   : SELL AMD
- Price    : $453.57
- Amount   : $47.01 | Shares: 0.103631
- RSI      : 23.7 | EMA: BEARISH | BB: BELOW_BAND
- RL       : BUY conf=1.0 | null (no veto)
- Stop     : $484.89 (trail_stop) | Target: $530.73
- Strategy : normal | Sell date: ATR/signal
- Regime   : bearish_ema
- Reason   : ATR trailing stop triggered: $453.57 ≤ trail_stop $484.89. AMD fell -6.0% from avg $482.48. Trail_stop ratcheted up to $484.89 when AMD was +2.6% ($495.07). Hours held: ~21h.

---

## 2026-07-28T14:20:51Z
- SUMMARY: Market open (10:20 ET). No trades executed. Buying power: $50.28. Equity positions: 1 (AMD). Regime: bearish_ema. Account: $96.38.
- AMD: $495.07 (+2.6% from avg $482.48), trail_stop=$484.89 (no change). No stop/take-profit triggers.
- BUY candidates: LITE RSI=28.2 conf=2->3 (RL BOOST, rl_conf=1.0) -- skipped: buying_power $50.28 < $50 buffer + $15 min order. NVDA RSI=29.1 conf=2 -- skipped: net_buy SELL + RL HOLD.
- SELL signals: JPM, GM (RSI overbought), GS/NVDA/CRM/SOUN/NOW/HOOD/GOOGL (net-buy sell) -- none held.
- CB: INACTIVE | daily 0.0% | weekly -3.9% (week_start $100.28)

---

## 2026-07-27T20:15:53Z
- SUMMARY: Market closed. Buying power: $50.28. Equity positions: 1 (AMD). Regime: bearish_ema. Account: $101.58.
- AMD: $495.07 (+2.6% from avg $482.48), trail_stop ratcheted $457.71→$484.89 (profit≥2.5%).
- Signals: BUY [NVDA RSI=29.1 conf=2, LITE RSI=28.1 conf=2] — not executed (market closed).
- Net-sell: [GS, NVDA, CRM, SOUN, NOW, HOOD, GOOGL] — none held.
- Surge: [RGTI, MCD] — not actioned (market closed).
- CB: INACTIVE | daily +1.3% | weekly +1.3%

---

## 2026-07-27T18:16:17Z
- Action   : BUY AMD
- Price    : $482.31
- Amount   : $50.00 | Shares: 0.10366
- RSI      : 26.8 | EMA: BEARISH | BB: BELOW_BAND
- RL       : BUY conf=1.0 | BOOST (2/3 → 3/3)
- Stop     : $457.71 | Target: $530.54
- Strategy : normal | Sell date: ATR/signal
- Regime   : bearish_ema
- Reason   : RSI oversold+stabilizing (28.0≈26.8) | BB reversal: -0.03→0.04 (returning from band) | RL BOOST applied

---

## 2026-07-27T17:14:28Z
- SUMMARY: Market OPEN (1:14 PM ET). No trades placed. Regime: bearish_ema (SPY $737.06 < EMA200 $744.31). RSI BUY: INTC (2/3, RSI 23.8, RL HOLD 0.886) — excluded (bearish_ema requires 3/3 confidence). RSI SELLs (not held): CRM (RSI 72.6), JNJ (RSI 79.0), GM (RSI 70.4), NOW (RSI 72.2). Net-buy SELLs (not held): GS, AMKR, C, HOOD, TGT, ASML, ONDS, NVDA, WFC, MU. Net-buy BUYs: none. Surge tracker: DIS count=1 buy-vol surge (needs count≥2 for intraday_surge entry). CB: INACTIVE | daily 0.0% | weekly 0.0%. Buying power: $100.28. Equity positions: 0. Account: $100.28. Peak: $101.68.

---

## 2026-07-27T16:20:00Z
- SUMMARY: Market OPEN (12:20 PM ET). No trades placed. Regime: bearish_ema (SPY $737.49 < EMA200 $744.38). RSI BUY signals: CVX (2/3) — excluded (bearish_ema requires 3/3). RSI SELLs: AAPL (RSI 70.5), CRM (RSI 70.9), JNJ (RSI 79.3) — not held. Net-buy SELLs: AMKR, GS, HOOD, C, ASML, TGT, SYM, WFC, SHOP, NOW — not held. Net-buy BUYs: none. Surge signals: none. CB: INACTIVE | daily 0.0% | weekly 0.0%. Buying power: $100.28. Equity positions: 0. Account: $100.28. Peak: $101.68.

---

## 2026-07-27T15:21:29Z
- SUMMARY: Market OPEN (11:21 AM ET). No trades placed — regime bearish_ema requires 3/3 confidence for buys; no qualifying signals. RSI SELLs (2/3, not held): AAPL (RSI 74.3 overbought), JPM (RSI 76.5 overbought), JNJ (RSI 79.7 overbought), GM (RSI 70.4 overbought). Net-buy BUY signals: none. Net-buy SELLs (not held): HOOD, AMKR, GEV, GS, TGT, CRM, NOW, SHOP, SYM. Surge signals: none. CB: INACTIVE | daily 0.00% | weekly 0.00%. Buying power: $100.28. Equity positions: 0. Regime: bearish_ema (SPY $739.69 < EMA200 $744.45). Account: $100.28. Peak: $101.68.

---

## 2026-07-27T14:21:39Z
- SUMMARY: Market OPEN (10:21 AM ET). No trades placed — regime bearish_ema requires 3/3 confidence for all buys. RSI BUY: RIVN (2/3, RSI 29.5, RL HOLD 0.919), MRNA (2/3, RSI 20.3, RL HOLD 0.886) — both excluded (bearish_ema 3/3 rule). RSI SELL: JPM (2/3, overbought 70.9), JNJ (2/3, overbought 72.8) — not held. Net-buy BUY: JNJ — conflicts with RSI SELL, skip. Net-buy SELLs: MBLY, UBER, MSFT, ALAB, PLTR, META, MCD, AI, SBUX, AMZN — not held. Surge signals: none. CB: INACTIVE | daily 0.00% | weekly 0.00% (new week reset — Monday 2026-07-27). Buying power: $100.28. Equity positions: 0. Regime: bearish_ema (SPY $738.85 < EMA200 $744.50). Account: $100.28. Peak: $101.68.

---
