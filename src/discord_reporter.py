import requests
import json
import os

DISCORD_WEBHOOK = os.getenv("DISCORD_WEBHOOK_URL", "")

def send_discord_report(report_path, summary=None):
    if not DISCORD_WEBHOOK:
        print("⚠️ Discord webhook not configured, skipping report dispatch.")
        return

    with open(report_path, "r", encoding="utf-8") as f:
        content = f.read()

    payload = {
        "username": "Digital Sentinel",
        "content": f"🧠 **New Quantum Report Uploaded**\nSummary:\n{summary or 'No summary provided'}",
        "embeds": [
            {"title": "Report File", "description": f"```json\n{content[:1500]}\n```"}
        ]
    }

    try:
        response = requests.post(DISCORD_WEBHOOK, json=payload)
        if response.status_code == 204:
            print("✅ Discord report sent successfully.")
        else:
            print(f"⚠️ Discord report failed → HTTP {response.status_code}")
    except Exception as e:
        print(f"⚠️ Discord reporting error: {e}")
