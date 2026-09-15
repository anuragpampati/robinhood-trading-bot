# Cloud routine prompts (reference copies)

These are reference copies of the prompts deployed to the three claude.ai scheduled
cloud routines ("CCR"s) that actually execute real trades. **Editing these files does
nothing** — the routines don't read from this repo's prompt files, they have their own
copy of the prompt text stored in the routine config, fetched fresh from GitHub only for
the code (`strategy/*.py`, `requirements.txt`, etc.) it runs each cycle.

To actually change a routine's behavior: update it via the `schedule` skill / `RemoteTrigger`
tool, then copy the new prompt text back into the matching file here so this stays a
truthful record of what's live.

| File | Routine name | Schedule |
|------|-------------|----------|
| `equity_prompt.txt` | Robinhood Trading Cycle | hourly, 10am-4pm ET Mon-Fri |
| `crypto_prompt.txt` | Robinhood Crypto Trading Cycle | daily, 1am UTC |

A fourth routine, "Robinhood Daily Learner" (4:30pm ET Mon-Fri, backtests recent trades
and auto-tunes `RSI_OVERSOLD` / `MOMENTUM_VOL_MIN` / `ATR_VOLATILITY_THRESHOLD` in
`strategy/config.py` if the data supports it), isn't mirrored here yet.

A fifth, "Options Trading — Daily RSI System", is currently **disabled** (options halted
pending a bigger backtest sample) — its prompt isn't mirrored here either.
