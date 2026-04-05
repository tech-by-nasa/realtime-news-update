"""
⏰ KEEPALIVE PINGER
====================
Free-tier services sleep when nobody visits.
Run this from ANY always-on machine (your laptop, a cron job, 
GitHub Actions, etc.) to keep your services awake.

Or set up a free uptime monitor at https://uptimerobot.com
"""

import requests
import time
import os

# Your service URLs (replace with your real ones)
RENDER_N8N_URL = os.environ.get(
    "RENDER_N8N_URL", 
    "https://magic-alert-brain.onrender.com/healthz"
)
HF_SPACE_URL = os.environ.get(
    "HF_SPACE_URL",
    "https://YOUR-USERNAME-magic-alert-box.hf.space"
)

PING_INTERVAL = 600  # 10 minutes (Render sleeps after 15)


def ping(url: str, name: str):
    """Send a GET request to keep the service awake."""
    try:
        resp = requests.get(url, timeout=30)
        status = "✅ AWAKE" if resp.status_code < 500 else "⚠️ ERROR"
        print(f"[{time.strftime('%H:%M:%S')}] {name}: {status} ({resp.status_code})")
    except Exception as e:
        print(f"[{time.strftime('%H:%M:%S')}] {name}: ❌ DOWN ({str(e)[:50]})")


def main():
    print("⏰ Keepalive Pinger Started!")
    print(f"   Pinging every {PING_INTERVAL} seconds...")
    print(f"   n8n: {RENDER_N8N_URL}")
    print(f"   HF:  {HF_SPACE_URL}")
    print("-" * 50)
    
    while True:
        ping(RENDER_N8N_URL, "n8n Brain")
        ping(HF_SPACE_URL, "HF Website")
        time.sleep(PING_INTERVAL)


if __name__ == "__main__":
    main()
