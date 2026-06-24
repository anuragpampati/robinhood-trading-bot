#!/usr/bin/env bash
# Automated trading cycle — runs via LaunchAgent every hour during market hours.
# Uses caffeinate to prevent Mac sleeping mid-run.
# Uses claude -p with Robinhood MCP (already authenticated locally).

cd /Users/anuragpampati/Desktop/Claude/robinhood

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
$PY -m strategy.run 2>/dev/null >> "$LOGFILE"
echo "[$TS] Signals generated." >> "$LOGFILE"

# ── Step 2: Claude executes trades via Robinhood MCP ─────────────────────────
cat > /tmp/rh_prompt.txt << 'EOF'
You are an automated trading agent for a $100 Robinhood agentic account. The signal file is at logs/latest_signals.json.

Do the following in order:
1. Run: cat logs/latest_signals.json
2. If market_open is false: print "MARKET_CLOSED" and stop.
3. Use the robinhood-trading MCP tools:
   - get_accounts → use account_number=837287598 (agentic_allowed=true)
   - get_portfolio  → buying_power
   - get_equity_positions → open positions and their average_buy_price
4. SELL checks — for each position you hold, get current price via get_equity_quotes:
   - If ticker in net_buy_sell_signals → SELL (print: SOLD <ticker> <shares> @ $<price> | signal)
   - If ticker in rsi_signals with action=SELL and confidence>=2 → SELL
   - If price <= avg_cost * 0.95 → SELL (print: SOLD <ticker> ... | STOP_LOSS)
   - If price >= avg_cost * 1.10 → SELL (print: SOLD <ticker> ... | TAKE_PROFIT)
5. BUY checks — capital rules (HARD LIMITS — never violate):
   - Keep >=$ 10 cash buffer at all times
   - Max $20 per new position, min $5
   - Max 4 open positions total — skip if len(held) >= 4
   - Never buy a ticker you already hold
   - Skip if SPY RSI < 40 in rsi_signals (market regime filter — broad market too weak)
   Priority:
   a. Ticker in BOTH net_buy_buy_signals (trend_days>=3) AND rsi_signals (action=BUY, confidence>=2) → $20
   b. Ticker in net_buy_buy_signals (trend_days>=3) only → $15
   c. Ticker in rsi_signals (action=BUY, confidence>=2) only → $15
   Print: BOUGHT <ticker> $<amount> @ $<price>
6. Print a one-line summary: "SUMMARY: <actions taken or 'no trades'>"

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
# Pull latest from cloud agent first so we don't overwrite docs/trade_log.md
git pull --rebase origin main 2>/dev/null || true

# Mirror signals to docs/ (safe — cloud agent also writes this)
cp logs/latest_signals.json docs/signals.json 2>/dev/null

# Prepend new trade log entry to docs/trade_log.md (don't copy — cloud agent owns it)
DOCS_LOG="docs/trade_log.md"
TMP_ENTRY="/tmp/rh_log_entry.md"
{
  echo "## $TS"
  if echo "$CLAUDE_OUTPUT" | grep -q "MARKET_CLOSED"; then
      echo "- Market closed — no trades placed."
  else
      echo "$CLAUDE_OUTPUT" | grep -E "^(BOUGHT|SOLD|STOP_LOSS|TAKE_PROFIT|SUMMARY)" | while read -r line; do
          echo "- $line"
      done
  fi
  echo ""
} > "$TMP_ENTRY"

if [ -f "$DOCS_LOG" ]; then
    # Prepend after the 5-line header block
    HEADER=$(head -5 "$DOCS_LOG")
    BODY=$(tail -n +6 "$DOCS_LOG")
    { printf "%s\n\n" "$HEADER"; cat "$TMP_ENTRY"; printf "%s\n" "$BODY"; } > "$DOCS_LOG.tmp" && mv "$DOCS_LOG.tmp" "$DOCS_LOG"
else
    { printf "# Trade Log — Robinhood Agentic Account\n\n> Auto-maintained by Claude agent. One entry per trade action.\n\n---\n\n"; cat "$TMP_ENTRY"; } > "$DOCS_LOG"
fi
rm -f "$TMP_ENTRY"

git add logs/trade_log.md logs/latest_signals.json docs/signals.json docs/trade_log.md 2>/dev/null
git diff --staged --quiet 2>/dev/null || \
    git commit -m "chore: trading cycle $TS" 2>/dev/null && \
    git push 2>/dev/null &

echo "[$TS] Cycle complete." >> "$LOGFILE"

# Stop caffeinate
kill $CAFPID 2>/dev/null
rm -f /tmp/rh_prompt.txt
