# Robinhood Trading Bot — Setup & Operations Guide

## What's Running

| Service | What it does |
|---------|-------------|
| `com.robinhood.trading` | Runs trading cycles hourly, Mon–Fri 10am–4pm ET |
| `com.robinhood.dashboard` | Flask dashboard server on `localhost:5001` |
| `com.robinhood.tunnel` | Cloudflare tunnel → public remote URL |

---

## Accessing the Dashboard

### From your Mac
Open **http://localhost:5001** in your browser.

### From anywhere (remote)
1. Open **http://localhost:5001** on your Mac
2. The blue banner at the top shows your current public URL (e.g. `https://xyz.trycloudflare.com`)
3. Open that URL on any device, anywhere

> The remote URL changes every time your Mac reboots. Always check the banner on localhost:5001 for the latest one.

### Login password
```bash
cat ~/.robinhood_token
```

---

## Running a Trade Cycle Manually

**Option A — Dashboard (recommended)**
1. Open `http://localhost:5001` or your tunnel URL
2. Log in
3. Click **▶ Run Now**
4. Watch the status bar for progress

**Option B — Terminal**
```bash
cd ~/robinhood
/bin/bash auto_trade.sh
```

**Option C — Claude Code chat**
Just say "run it" in this chat and Claude will run a full cycle via MCP.

---

## Automatic Schedule

Runs every hour, Monday–Friday, 10am–4pm ET (7am–1pm PDT):

| ET | PDT | UTC |
|----|-----|-----|
| 10:00 AM | 7:00 AM | 14:00 |
| 11:00 AM | 8:00 AM | 15:00 |
| 12:00 PM | 9:00 AM | 16:00 |
| 1:00 PM  | 10:00 AM | 17:00 |
| 2:00 PM  | 11:00 AM | 18:00 |
| 3:00 PM  | 12:00 PM | 19:00 |
| 4:00 PM  | 1:00 PM  | 20:00 |

---

## Reloading Services (after reboot or config changes)

```bash
# Trading agent
launchctl unload ~/Library/LaunchAgents/com.robinhood.trading.plist
launchctl load  ~/Library/LaunchAgents/com.robinhood.trading.plist

# Dashboard server
launchctl unload ~/Library/LaunchAgents/com.robinhood.dashboard.plist
launchctl load  ~/Library/LaunchAgents/com.robinhood.dashboard.plist

# Cloudflare tunnel
launchctl unload ~/Library/LaunchAgents/com.robinhood.tunnel.plist
launchctl load  ~/Library/LaunchAgents/com.robinhood.tunnel.plist
```

Check all three are running:
```bash
launchctl list | grep robinhood
```
All three should show exit code `0`.

---

## Checking Logs

```bash
# Last trading cycle output
tail -50 ~/robinhood/logs/auto_run.log

# Trade history
cat ~/robinhood/logs/trade_log.md

# Dashboard server log
cat ~/robinhood/logs/dashboard.log

# Tunnel log
cat ~/robinhood/logs/tunnel.log

# Current remote URL
cat ~/robinhood/logs/tunnel_url.txt
```

---

## Project Structure

```
~/robinhood/
├── auto_trade.sh          # Main trading cycle script
├── server.py              # Dashboard Flask server (port 5001)
├── start_tunnel.sh        # Cloudflare quick tunnel
├── cloudflared            # Cloudflare binary
├── strategy/              # Signal generation (RSI, net-buy, VWAP)
├── docs/                  # GitHub Pages dashboard
│   ├── index.html
│   ├── signals.json
│   ├── positions.json
│   └── trade_log.md
├── logs/
│   ├── auto_run.log       # Cycle output
│   ├── trade_log.md       # Trade history
│   ├── latest_signals.json
│   ├── tunnel_url.txt     # Current public URL
│   └── launchagent.log
└── ~/Library/LaunchAgents/
    ├── com.robinhood.trading.plist
    ├── com.robinhood.dashboard.plist
    └── com.robinhood.tunnel.plist
```

---

## Strategy Rules (Quick Reference)

| Rule | Value |
|------|-------|
| Account size | $100 |
| Min cash buffer | $10 |
| Max per position | $20 |
| Max positions | 4 |
| Stop-loss | −5% from entry |
| Take-profit | +10% from entry |
| Watchlist | SPY, QQQ, AAPL, MSFT, NVDA |

**Buy when:** signal BUY + confidence ≥ 2 + market open + not within 30min of open/close  
**Sell when:** SELL signal OR stop-loss hit OR take-profit hit

---

## GitHub Pages (Read-Only Dashboard)

**URL:** https://anuragpampati.github.io/robinhood-trading-bot/

Shows live signals and trade history. No login or Run button — view only.
Updates automatically after every trade cycle via `git push`.
