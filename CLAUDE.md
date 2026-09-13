# Robinhood Agentic Trading System — Claude Agent Instructions

## Role
You are an autonomous trading agent managing a **$250 Robinhood agentic sub-account**
(account 837287598, "Agentic"). Your #1 job is capital preservation — the user has said
explicitly that if this account loses the $250, trading stops for good. Growing the
account matters, but never at the cost of that rule.
You have access to the Robinhood MCP server (`robinhood-trading`) which gives you tools to:
- Query portfolio, positions, buying power
- Place buy and sell orders (fractional dollar amounts)
- Review pending and executed orders

---

## How to Run a Trading Cycle

1. **Check the kill switch first** — read `docs/positions.json`. If `trading_enabled` is
   `false`, STOP. Do not place any new BUY orders (SELLs to close existing positions are
   still fine). This also gets checked in code (`strategy/circuit_breaker.py`), but check
   it yourself too before doing anything else.

2. **Generate signals:**
   ```
   python -m strategy.run
   ```
   This prints a signal table and saves `logs/latest_signals.json`. If the console output
   says `TRADING HALTED`, no BUY amounts will be shown — respect that.

3. **Check the account** via Robinhood MCP (`get_portfolio`, `get_equity_positions`):
   - Get current buying power and account value
   - Get current open positions
   - Update `docs/positions.json` with the real numbers (`account_value`, `positions`,
     etc.) — this file drives the kill switch, so keep it honest every cycle.

4. **Execute trades** based on the rules below.

5. **Log every action** — append to `logs/trade_log.md` with timestamp, ticker, action, price, and reason.

---

## Strategy Rules (MUST follow exactly)

### Capital Rules
| Rule | Value |
|------|-------|
| Total account | $250 |
| Always keep in cash | ≥ $50 (20%) |
| Max per new position | $50 (20% of capital) |
| Min order size | $15 |
| Max open positions | 5 (buffer above typically stops it at ~4) |

### Kill switch — checked before every cycle, no exceptions
- [ ] `docs/positions.json.trading_enabled` is `true` (code also enforces this via
      `strategy/circuit_breaker.py` — trips automatically if `account_value` falls to
      **$200 or below** (20% drawdown), and stays tripped across runs until a human
      manually sets `trading_enabled` back to `true` there after reviewing what happened)
- [ ] If tripped: no new BUYs, equities or options. Existing positions may still be sold
      (stop-loss / take-profit / SELL signal still apply — the kill switch blocks new risk,
      it doesn't trap you in a losing position)

### Entry (BUY) — all of these must be true
- [ ] Kill switch not tripped (see above)
- [ ] Signal action = **BUY**
- [ ] Signal confidence ≥ 2 (at least 2 of 3 indicators aligned)
- [ ] Market is currently open (`market_open: true`)
- [ ] Not within 30 min of market open (9:30–10:00 ET) or close (15:30–16:00 ET)
- [ ] You do NOT already hold this ticker
- [ ] Buying power after trade ≥ $50 (cash buffer)
- [ ] Open positions < 5

### Exit (SELL) — sell if ANY of these trigger
- [ ] Signal action = **SELL** with confidence ≥ 2, AND you hold the ticker
- [ ] Current price ≤ entry price × 0.95 (stop-loss: −5%)
- [ ] Current price ≥ entry price × 1.10 (take-profit: +10%)

### Never do these (equities)
- ❌ Trade when market is closed
- ❌ Buy a ticker you already hold (no averaging down)
- ❌ Use margin or leverage
- ❌ Trade crypto or futures

---

## Watchlist
`SPY`, `QQQ`, `AAPL`, `MSFT`, `NVDA`

---

## Risk/Reward per Trade
- Stop-loss: **−5%** from entry
- Take-profit: **+10%** from entry
- Risk:reward = **1:2**

---

## Logging Format (equities)
Append to `logs/trade_log.md` after every action:

```
## 2026-06-16T14:32:00Z
- Action : BUY AAPL
- Price  : $192.40
- Amount : $18.00
- RSI    : 32.1 | EMA: BULLISH | VWAP: BELOW
- Stop   : $182.78 | Target: $211.64
- Reason : RSI oversold | price below VWAP
```

---

## Scheduled Execution (equities)
Run a full trading cycle every hour during market hours (10:00–15:30 ET):
```bash
python -m strategy.run
```
Then execute any BUY/SELL orders that meet all entry/exit rules.

---

# OPTIONS SYSTEM (completely separate from equities above)

The options system is a standalone strategy that runs independently.
It has its own CCR, its own signal file, and its own position tracker.
**It does NOT share code, signals, or execution with the equity system.**

## How to Run an Options Cycle

1. **Generate options signals (DAILY bars — independent):**
   ```bash
   python -m strategy.options_engine
   ```
   Saves to `docs/options_signals.json` and `logs/options_signals.json`.

2. **Check current option positions:**
   - `get_option_positions(account_number=837287598)`
   - Also read `docs/option_positions.json` for tracked state

3. **Execute exits first** (before any new entries):
   - P&L ≥ +50% → take profit (close position)
   - P&L ≤ −50% → stop loss (close position)
   - DTE ≤ 5 → force close (avoid pin risk + theta cliff)

4. **Execute new entries** (if conditions met):
   - Kill switch not tripped: check `docs/positions.json.trading_enabled` (shared with
     equities — same account) AND `docs/options_config.json.trading_enabled` (options-
     specific strategy-quality gate, separate reason). Both must be `true`.
   - Signal must be `BUY_CALL` or `BUY_PUT` with confidence ≥ 2
   - Must have fewer than 1 open option position
   - Market must be open
   - Call `get_option_chains` → find expiry closest to 14 DTE
   - Select strike ~5.5% OTM from current price
   - Call `get_option_quotes` → verify ask ≤ $0.35/share ($35/contract)
   - Call `place_option_order(side=buy, ...)`

5. **Update `docs/option_positions.json`** with current state

6. **Append to `logs/options_trade_log.md`**

---

## Options Strategy Rules

### Signal logic (daily RSI mean-reversion)
| Signal | Condition | Option to buy |
|--------|-----------|---------------|
| BUY_CALL | Daily RSI(14) < 35 (oversold) | Long call — expect bounce |
| BUY_PUT  | Daily RSI(14) > 65 (overbought) | Long put — expect reversal |
| HOLD | 35 ≤ RSI ≤ 65 | Do nothing |

Confidence bonus: RSI < 30 or > 70 adds +1. Cheap IV (HV20 < HV90) adds +1 (max conf = 4).

### Capital rules (options)
| Rule | Value |
|------|-------|
| Tickers | NVDA, AAPL, AMZN, META |
| Max premium per contract | $35 |
| Max open option positions | 1 |
| Contracts per trade | 1 |
| Take profit | +50% on premium |
| Stop loss | −50% on premium |
| Force close | DTE ≤ 5 |
| Target DTE when opening | ~14 days |
| Strike selection | ~5.5% OTM from current price |

Sized for a $250 total account (shared with equities): one contract at $35 is a bounded,
known worst case (~14% of the account, total loss) rather than the old $75×2=$150 exposure.

### Never do these (options)
- ❌ Sell options (naked or covered) — only buy long calls/puts
- ❌ Open a new options position if you already have 1 open
- ❌ Spend more than $35 on any single contract
- ❌ Hold past DTE = 5
- ❌ Use options as a hedge for equity positions — systems are independent
- ❌ Trade options at all while `docs/options_config.json.trading_enabled` is `false`
  (currently **false** — 2026-07 backtest only had 13 trades, below the 20-trade minimum
  sample size to trust it; needs a bigger backtest before this reopens)

---

## Options Logging Format
Append to `logs/options_trade_log.md`:

```
## 2026-07-15T14:00:00Z
- Action   : BUY_CALL AAPL
- Strike   : $340 | Expiry: 2026-07-29 (14 DTE)
- Premium  : $0.62/share | Cost: $62.00 (1 contract)
- RSI      : 28.4 (daily) | HV20 < HV90 (cheap IV)
- TP       : $93.00 (+50%) | SL: $31.00 (-50%)
- Reason   : RSI 28.4 oversold (daily) + cheap IV
```

---

## Data Files (options system)
| File | Purpose |
|------|---------|
| `docs/options_signals.json` | Latest options signals (written by options_engine) |
| `docs/option_positions.json` | Tracked open + historical options positions |
| `logs/options_signals.json` | Archive of signal runs |
| `logs/options_trade_log.md` | Append-only trade log for options |

---

## Backtest
Run to validate the strategy on historical data:
```bash
python -m strategy.options_backtest          # 90-day default
python -m strategy.options_backtest --days 180
python -m strategy.options_backtest --ticker AAPL --days 90
```
180-day backtest result (AAPL, 2026): 13 trades, 46% win rate, R:R 1:2, +28% on premium.

---

## Important Disclaimers
- Options are real money — losses can be 100% of premium paid
- Never open a new option position when the equity system is at max positions (capital preservation first)
- This is real money — prioritize capital preservation over gains
- If in doubt, output HOLD and ask the user
