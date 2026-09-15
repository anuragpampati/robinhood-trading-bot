#!/usr/bin/env bash
# Automated trading cycle — runs via LaunchAgent every hour during market hours.
# Uses caffeinate to prevent Mac sleeping mid-run.
# Uses claude -p with Robinhood MCP (already authenticated locally).

cd "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

LOGFILE="logs/auto_run.log"
TRADELOG="logs/trade_log.md"
PY="/Users/anuragpampati/anaconda3/bin/python3"
CLAUDE="/Users/anuragpampati/.local/bin/claude"
TS=$(date '+%Y-%m-%d %H:%M:%S')

# Prevent Mac from sleeping during this run
caffeinate -i -t 300 &
CAFPID=$!

echo "" >> "$LOGFILE"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" >> "$LOGFILE"
echo "[$TS] Starting trading cycle" >> "$LOGFILE"

# ── Step 1: Generate signals ──────────────────────────────────────────────────
# --quick: curated watchlist, not full-universe. Backtested 2026-09-15: full
# universe (~503 S&P 500 tickers) underperforms the curated watchlist
# significantly (-4.8% vs +5.9% over the same 90-day window) -- more tickers
# surfaced more low-quality mean-reversion setups, not better ones.
$PY -m strategy.run --quick 2>/dev/null >> "$LOGFILE"
echo "[$TS] Signals generated." >> "$LOGFILE"

# ── Step 2: Claude executes trades via Robinhood MCP ─────────────────────────
cat > /tmp/rh_prompt.txt << 'EOF'
You are an automated trading agent for a $250 Robinhood agentic account. The signal file is at logs/latest_signals.json.

Do the following in order:
1. Run: cat logs/latest_signals.json
2. If market_open is false: print "MARKET_CLOSED" and stop.
3. If trading_halted is true in that file: print "TRADING_HALTED: <halt_reason>" and stop.
   Do NOT place any new BUY orders. (SELL checks in step 5 still apply — the kill
   switch blocks new risk, it does not trap you in a losing position.)
4. Use the robinhood-trading MCP tools:
   - get_accounts → use account_number=837287598 (agentic_allowed=true)
   - get_portfolio  → buying_power, account value
   - get_equity_positions → open positions and their average_buy_price
5. SELL checks — for each position you hold, get current price via get_equity_quotes:
   - If ticker in net_buy_sell_signals → SELL (print: SOLD <ticker> <shares> @ $<price> | signal)
   - If ticker in rsi_signals with action=SELL and confidence>=2 → SELL
   - If price <= avg_cost * 0.95 → SELL (print: SOLD <ticker> ... | STOP_LOSS)
   - If price >= avg_cost * 1.10 → SELL (print: SOLD <ticker> ... | TAKE_PROFIT)
6. BUY checks (skip entirely if step 3 halted trading) — capital rules (HARD LIMITS — never violate):
   - Keep >=$50 cash buffer at all times
   - Max $50 per new position (2/3 confidence) or $50 at 3/3 confidence, $25 at 2/3 — min $15
   - Max 5 open positions total — skip if len(held) >= 5
   - Never buy a ticker you already hold
   - Skip if SPY RSI < 30 in rsi_signals (market regime filter — broad market panic)
   Priority:
   a. Ticker in BOTH net_buy_buy_signals (trend_days>=3) AND rsi_signals (action=BUY, confidence>=3) → $50
   b. Ticker in rsi_signals (action=BUY, confidence>=2) only, or net_buy_buy_signals only → $25
   Print: BOUGHT <ticker> $<amount> @ $<price>
7. Print a one-line summary: "SUMMARY: <actions taken or 'no trades'>"

Only print actions you actually took. Do not write to any files.
EOF

echo "[$TS] Running Claude trade executor..." >> "$LOGFILE"
CLAUDE_OUTPUT=$(cat /tmp/rh_prompt.txt | "$CLAUDE" -p \
    --allowedTools "mcp__robinhood-trading__get_accounts,mcp__robinhood-trading__get_portfolio,mcp__robinhood-trading__get_equity_positions,mcp__robinhood-trading__get_equity_orders,mcp__robinhood-trading__get_equity_quotes,mcp__robinhood-trading__get_equity_tradability,mcp__robinhood-trading__place_equity_order,mcp__robinhood-trading__review_equity_order,mcp__robinhood-trading__cancel_equity_order,Bash" \
    2>/dev/null)

echo "$CLAUDE_OUTPUT" >> "$LOGFILE"

# ── Step 3: Write to trade log ────────────────────────────────────────────────
echo "" >> "$TRADELOG"
echo "## $TS" >> "$TRADELOG"

if echo "$CLAUDE_OUTPUT" | grep -q "MARKET_CLOSED"; then
    echo "- Market closed — no trades placed." >> "$TRADELOG"
else
    echo "$CLAUDE_OUTPUT" | grep -E "^(BOUGHT|SOLD|STOP_LOSS|TAKE_PROFIT|SUMMARY)" | while read -r line; do
        echo "- $line" >> "$TRADELOG"
    done
fi

# ── Step 4: Sync logs to GitHub ───────────────────────────────────────────────
# docs/trade_log.md and docs/positions.json are owned exclusively by the cloud
# agent — never touch them here to avoid race conditions.
# This script only updates logs/ and docs/signals.json.
cp logs/latest_signals.json docs/signals.json 2>/dev/null

git pull --rebase origin main 2>/dev/null || true
git add logs/trade_log.md logs/latest_signals.json docs/signals.json 2>/dev/null
git diff --staged --quiet 2>/dev/null || \
    git commit -m "chore: trading cycle $TS" 2>/dev/null && \
    git push 2>/dev/null &

echo "[$TS] Cycle complete." >> "$LOGFILE"

# Stop caffeinate
kill $CAFPID 2>/dev/null
rm -f /tmp/rh_prompt.txt
