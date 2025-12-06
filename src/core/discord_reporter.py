import json
import os
import requests
from datetime import datetime

def send_discord_report():
    print("📡 [Phase 9: Discord Reporter Started]")

    # Path to AI report
    report_path = "data/reports/ai_intel_summary.json"

    # Check existence
    if not os.path.exists(report_path):
        print("⚠️ No AI report found. Skipping Discord notification.")
        return

    with open(report_path, "r") as f:
        data = json.load(f)

    # Discord Webhook URL (💡 set this in GitHub Secrets)
    webhook_url = os.getenv("DISCORD_WEBHOOK_URL")
    if not webhook_url:
        print("⚠️ Discord webhook not configured. Please set DISCORD_WEBHOOK_URL in secrets.")
        return

    # Build embed message
    embed = {
        "username": "🛡️ Digital Sentinel AI",
        "avatar_url": "https://i.imgur.com/nvZH2Hk.png",
        "embeds": [
            {
                "title": "📊 Digital Sentinel Quantum Infinity - AI Summary Report",
                "description": f"**AI Layer Assessment:** {data.get('ai_assessment', 'N/A')}",
                "color": 15158332 if "High" in data.get("ai_assessment", "") else 3066993,
                "fields": [
                    {"name": "🕒 Timestamp", "value": data.get("timestamp", "N/A"), "inline": False},
                    {"name": "📈 Total Findings", "value": str(data.get("total_findings", 0)), "inline": True},
                    {"name": "🔥 High Risk", "value": str(data.get("high_risk_count", 0)), "inline": True},
                    {"name": "⚠️ Medium Risk", "value": str(data.get("medium_risk_count", 0)), "inline": True},
                    {"name": "🟢 Low Risk", "value": str(data.get("low_risk_count", 0)), "inline": True},
                ],
                "footer": {
                    "text": f"Sent by Digital Sentinel at {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}"
                },
            }
        ],
    }

    # Send to Discord
    response = requests.post(webhook_url, json=embed)

    if response.status_code == 204:
        print("✅ Discord notification sent successfully.")
    else:
        print(f"❌ Failed to send Discord message. Status: {response.status_code}")
        print(response.text)

    print("📡 [Phase 9 Completed: Discord Report Sent]")
