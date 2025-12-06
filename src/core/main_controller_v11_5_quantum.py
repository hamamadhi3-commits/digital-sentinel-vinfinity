import os
import json
import requests
from datetime import datetime

def run_discord_reporter():
    """
    Sends a final AI summary report to Discord via webhook.
    Uses the secret DISCORD_WEBHOOK_URL from GitHub Actions environment.
    """
    print("📡 [Phase 9: Discord Reporter Started]")

    webhook_url = os.getenv("DISCORD_WEBHOOK_URL")

    if not webhook_url:
        print("⚠️ Discord webhook not configured. Please set DISCORD_WEBHOOK_URL in secrets.")
        return

    # هەوڵدەدات ڕاپۆرتی intelligence summary بنێرێت بۆ Discord
    report_path = "data/reports/ai_intel_summary.json"
    report_data = {}
    if os.path.exists(report_path):
        with open(report_path, "r") as f:
            report_data = json.load(f)
    else:
        report_data = {"message": "No report data found."}

    content = {
        "username": "🛰️ Digital Sentinel",
        "embeds": [{
            "title": "Digital Sentinel Quantum Infinity Report",
            "description": f"🧠 Intelligence Summary — {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}",
            "color": 16753920,
            "fields": [
                {"name": "Status", "value": "✅ Scan completed successfully", "inline": False},
                {"name": "Report Summary", "value": json.dumps(report_data, indent=2)[:1500] + "...", "inline": False},
            ],
            "footer": {"text": "Digital Sentinel vInfinity AI"}
        }]
    }

    try:
        response = requests.post(webhook_url, json=content)
        if response.status_code == 204:
            print("✅ Discord notification sent successfully.")
        else:
            print(f"⚠️ Discord webhook response: {response.status_code}")
    except Exception as e:
        print(f"❌ Failed to send Discord report: {e}")

    print("✅ [Phase 9: Discord Reporter Completed]")
