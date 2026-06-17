#!/usr/bin/env bash
# Starts a Cloudflare quick tunnel and writes the public URL to a file.
cd /Users/anuragpampati/robinhood
URLFILE="logs/tunnel_url.txt"
rm -f "$URLFILE"

/Users/anuragpampati/robinhood/cloudflared tunnel --url http://localhost:5001 2>&1 | \
while IFS= read -r line; do
    echo "$line"
    if [[ "$line" =~ https://[a-z0-9-]+\.trycloudflare\.com ]]; then
        echo "${BASH_REMATCH[0]}" > "$URLFILE"
    fi
done
