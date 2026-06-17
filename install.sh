#!/usr/bin/env bash
# One-time setup: installs LaunchAgent + configures lid-closed operation.

PROJ="/Users/anuragpampati/Desktop/Claude/robinhood"
PLIST="com.robinhood.trading.plist"
LAUNCH_DIR="$HOME/Library/LaunchAgents"

echo ""
echo "╔══════════════════════════════════════════════════╗"
echo "║  Robinhood Trading Bot — Mac Background Setup   ║"
echo "╚══════════════════════════════════════════════════╝"
echo ""

# 1. Remove old cron job
crontab -r 2>/dev/null && echo "[1/4] Removed old cron job." || echo "[1/4] No cron job to remove."

# 2. Install LaunchAgent
mkdir -p "$LAUNCH_DIR"
cp "$PROJ/$PLIST" "$LAUNCH_DIR/$PLIST"
launchctl unload "$LAUNCH_DIR/$PLIST" 2>/dev/null
launchctl load "$LAUNCH_DIR/$PLIST"
echo "[2/4] LaunchAgent installed and loaded."

# 3. Prevent system sleep when on charger (lid closed)
# Only disables sleep on AC power — battery still sleeps normally
sudo pmset -c sleep 0
echo "[3/4] Sleep disabled on AC power (Mac stays on when plugged in, lid closed)."

# 4. Keep display sleep normal (saves power, doesn't affect the bot)
sudo pmset -c displaysleep 30
echo "[4/4] Display sleep kept at 30 min (screen off = fine, system stays on)."

echo ""
echo "╔══════════════════════════════════════════════════╗"
echo "║  Done! Bot is now running automatically.         ║"
echo "║                                                  ║"
echo "║  Keep your Mac:  Plugged into power              ║"
echo "║  Lid:            Can be closed                   ║"
echo "║  Screen:         Will sleep (that's fine)        ║"
echo "║                                                  ║"
echo "║  Runs every hour Mon-Fri 10am-3pm ET             ║"
echo "║  Dashboard: anuragpampati.github.io/             ║"
echo "║             robinhood-trading-bot/               ║"
echo "╚══════════════════════════════════════════════════╝"
echo ""
echo "To check status:  tail -f logs/auto_run.log"
echo "To stop the bot:  launchctl unload ~/Library/LaunchAgents/com.robinhood.trading.plist"
echo "To re-enable:     launchctl load ~/Library/LaunchAgents/com.robinhood.trading.plist"
echo ""
