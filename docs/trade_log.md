# Trade Log — Robinhood Agentic Account

> Auto-maintained by Claude agent. One entry per trade action.

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
- Reason   : ATR trailing stop triggered: $453.57 ≤ trail_stop $484.89. AMD fell -6.0% from avg $482.48. Trail_stop was ratcheted up to $484.89 when AMD hit +2.6% ($495.07). Hours held: ~21h (entry 2026-07-27T18:16Z).

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

## 2026-07-24T20:13:07Z
- SUMMARY: Market CLOSED (after hours). No trades placed. Regime: bearish_ema (SPY $738.85 < EMA200 $744.44). RSI BUY signals: MRNA (2/3), RIVN (2/3) — both excluded (bearish_ema requires 3/3). RSI SELL: JPM (overbought 71.5), JNJ (overbought 73.1) — not held. Net-buy SELLs: MBLY, UBER, ALAB, MSFT, PLTR, MCD, META, AI, SBUX, AMZN — not held. Surge signals: none. CB: INACTIVE | daily −0.39% drawdown (account UP) | weekly −0.13%. Buying power: $50.24. Equity positions: 0. Account: $100.28. Peak: $101.68.

---

## 2026-07-24T16:12:01Z
- Action   : SELL PLTR
- Price    : $123.66
- Amount   : $50.04 | Shares: 0.404663
- RSI      : 35.0 | EMA: BEARISH | BB: IN_BAND
- RL       : null conf=null | null
- Stop     : $120.52 | Target: $135.92
- Strategy : normal | Sell date: ATR/signal
- Regime   : bearish_ema
- Reason   : Net buy reversed (1.30M → 0.04M) | OBV -4.0M/day | 25.9h held ≥ 3h → signal sell (rule c)

---

## 2026-07-24T16:12:30Z
- SUMMARY: Market OPEN (12:12 PM ET). SOLD PLTR @ $123.66 (net buy reversed, 25.9h held). No new buys — bearish_ema requires 3/3 conf; best signals AMZN RSI BUY 2/3 (also net-buy SELL), MRNA RSI BUY 2/3, TXN net-buy only — none qualify. Regime: bearish_ema (SPY $743.00 < EMA200 $744.63). CB: INACTIVE | daily +0.39% | weekly -0.13%. Buying power: ~$100.28 (post-sell). Equity positions: 0. Account: $100.28. Peak: $101.68.

---

## 2026-07-24T14:14:54Z
- SUMMARY: Market OPEN (10:14 AM ET). No trades placed. Buying power $50.24 — only $0.24 above $50 buffer (min order $15, no buys possible). Regime: bearish_ema (SPY $738.24 < EMA200 $744.68). PLTR: $122.63 (trail_stop $120.52 OK, pnl -0.75%, hours_held ~24.0h). No exit triggered (above trail_stop, no SELL signal, no take-profit). RSI BUY signals (9 tickers, all 2/3 conf — excluded by bearish_ema 3/3 requirement): CRM, AMZN, GOOGL, META, TSLA, MRNA, DIS, SHOP. UBER: 2/3 RSI BUY + RL BOOST→3/3 (rl_confidence 0.952) — buying power insufficient ($0.24 available after buffer). Net-buy SELLs: ORCL, CRWD, MBLY, TSLA, SHOP, GOOGL, RIVN, AAPL, UBER — none held. No surge signals. CB: INACTIVE | daily 0.00% (new day reset) | weekly 0.52%. Positions: 1 (PLTR). Buying power: $50.24. Account: $99.89. Peak: $101.68.

---

## 2026-07-23T20:10:31Z
- SUMMARY: Market CLOSED (after hours, ~4:10 PM ET). No trades. SPY $738.24 (RSI 32.8, EMA BEARISH — below EMA200 $744.65). Regime: bearish_ema (RSI 32.8 ≥ 30 — PANIC mode lifted). RSI BUY candidates (deferred — market closed): CRM, AMZN, GOOGL, META, TSLA, MRNA, DIS, TGT, UBER, SHOP (conf 2/3 each). Net-buy BUY: JPM. Net-buy SELLs: ORCL, TSLA, GOOGL, SHOP, AAPL, RIVN, MBLY, CRWD, UBER, QBTS — none held. PLTR: $123.30 (trail_stop $120.52 OK, pnl -0.21%, hours_held ~5.9h). No exit triggered (above trail_stop, no SELL signal, no take-profit). Trail_stop unchanged (pnl < 2.5%). CB: INACTIVE | daily 0.10% | weekly 0.27%. Positions: 1 (PLTR). Buying power: $50.24. Account: $100.14. Peak: $101.68.

---

## 2026-07-23T19:13:00Z
- SUMMARY: Market OPEN (3:13 ET) — PANIC+bearish_ema (SPY RSI 28.2 < 30, below EMA200 $744.72). No buys: PANIC mode suppresses all individual buys; buying power $50.24 = only $0.24 above $50 buffer. PLTR: $122.18 (trail_stop $120.52 not hit, pnl -1.12%, hours_held 4.9h). No exit triggered (ATR stop not hit, no SELL signal, no take-profit). RSI SELL (conf≥2): XOM (80.6) — not held. Net-buy SELLs: MBLY, ORCL, UBER, AAPL, TSLA, CRWD, RIVN, SPY, QBTS — not held. No surge signals. CB: INACTIVE | daily 0.58% | weekly 0.75%. Regime: bearish_ema/PANIC. Positions: 1 (PLTR). Buying power: $50.24. Account: $99.66. Peak: $101.68.

---

## 2026-07-23T18:11:52Z
- SUMMARY: Market OPEN (2:11 ET). No trades — PANIC regime (SPY RSI 28.4 < 30, bearish_ema), all individual stock buys suppressed. Also $50.24 buying power leaves only $0.24 above $50 buffer — no buys possible regardless. RSI SELL (conf≥2): XOM (81.9), CVX (75.1) — not held. Net-buy SELL: AAPL, CRWD, RIVN, TSLA, WMT, MBLY, ORCL — not held. PLTR: $122.27 (trail_stop $120.52 OK, pnl -1.04%, hours_held 3.9h). No exit triggered. CB: INACTIVE | daily 0.53% | weekly 0.70%. Regime: bearish_ema/PANIC (SPY $737.19 < EMA200 $744.80, RSI 28.4). Positions: 1 (PLTR). Buying power: $50.24. Account: $99.71. Peak: $101.68.

---

## 2026-07-23T16:14:06Z
- SUMMARY: Market OPEN (12:14 ET). No trades — PANIC regime (SPY RSI 27.8 < 30, bearish_ema), all individual stock buys suppressed. RSI SELL (conf≥2): XOM (84.3), MRCY (70.6) — not held. Net-buy SELL: MBLY, AAPL, CRWD, ORCL, SHOP — not held. No BUY signals. No surge signals. PLTR: $121.52 (trail_stop $120.52 OK, pnl -1.65%, hours_held 1.92h <3). CB: INACTIVE | daily 0.8% | weekly 1.0%. Regime: bearish_ema/PANIC (SPY $738.67 < EMA200 $744.94, RSI 27.8). Positions: 1 (PLTR). Buying power: $50.24. Account: $99.41. Peak: $101.68.

---

## 2026-07-23T14:17:22Z
- Action   : BUY PLTR
- Price    : $123.53
- Amount   : $50.00 | Shares: 0.40475
- RSI      : 29.6 | EMA: BEARISH | BB: BELOW_BAND
- RL       : HOLD conf=0.906 | null
- Stop     : $120.52 | Target: $135.88
- Strategy : normal | Sell date: ATR/signal
- Regime   : normal
- Reason   : RSI oversold+stabilizing (28.8↑29.6) | BB reversal: returning from lower band

---
