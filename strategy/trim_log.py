"""Trim logs/trade_log.md to the last N days (default 2)."""
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

DAYS = int(sys.argv[1]) if len(sys.argv) > 1 else 2
LOG  = Path("logs/trade_log.md")

if not LOG.exists():
    sys.exit(0)

cutoff = datetime.now(timezone.utc) - timedelta(days=DAYS)
text   = LOG.read_text()

# Split on section headers; first chunk is the file preamble (no timestamp)
parts = text.split("\n## ")
preamble = parts[0]
entries  = parts[1:]

kept = []
for e in entries:
    ts_str = e.split("\n")[0].strip()
    try:
        ts = datetime.fromisoformat(ts_str.replace("Z", "+00:00"))
        if ts.tzinfo is None:
            ts = ts.replace(tzinfo=timezone.utc)
        if ts >= cutoff:
            kept.append(e)
    except ValueError:
        kept.append(e)  # unparseable → keep

LOG.write_text(preamble + ("\n## " + "\n## ".join(kept) if kept else ""))
print(f"[trim_log] Kept {len(kept)}/{len(entries)} entries (last {DAYS} days)")
