# src/discord_reporter.py
import requests
import json
import os

def send_report(message: str, title: str = "Digital Sentinel Report"):
    """Send a formatted message to Discord webhook."""
    webhook_url = os.getenv("DISCORD_WEBHOOK_URL")
    if not webhook_url:
        print("❌ No DISCORD_WEBHOOK_URL found.")
        return

    payload = {
        "embeds": [
            {
                "title": title,
                "description": message,
                "color": 0x00FFAA
            }
        ]
    }

    try:
        response = requests.post(webhook_url, data=json.dumps(payload), headers={"Content-Type": "application/json"})
        if response.status_code == 204:
            print("✅ Discord report sent successfully.")
        else:
            print(f"⚠️ Discord returned {response.status_code}: {response.text}")
    except Exception as e:
        print(f"❌ Failed to send Discord message: {e}")
