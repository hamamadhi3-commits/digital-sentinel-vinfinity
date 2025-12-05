import os
import json
import requests
from datetime import datetime

def send_report(webhook_url: str):
    """Send scan summary report to Discord."""
    try:
        now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")

        # Find latest JSON report
        report_path = None
        for root, dirs, files in os.walk("data/results/final_reports"):
            for f in sorted(files, reverse=True):
                if f.endswith(".json"):
                    report_path = os.path.join(root, f)
                    break
            if report_path:
                break

        summary = "No report summary found."
        if report_path and os.path.exists(report_path):
            with open(report_path, "r", encoding="utf-8") as f:
                data = f.read()
                summary = data[:1500]  # Limit message size
        else:
            print("⚠️ No JSON report found, using fallback summary.")

        embed = {
            "title": "🛰 Digital Sentinel Quantum Infinity Report",
            "description": (
                f"**Cycle completed successfully!**\n\n"
                f"🕐 Timestamp: `{now}`\n"
                f"📁 Report File: `{report_path or 'Not found'}`\n\n"
                f"🧠 AI Summary:\n```{summary}```"
            ),
            "color": 0x00AEEF,
            "footer": {"text": "Digital Sentinel v∞ Quantum Controller"},
            "thumbnail": {
                "url": "https://i.imgur.com/3Nczd8V.png"
            },
        }

        files = None
        # ✅ Upload JSON report as file if exists
        if report_path and os.path.exists(report_path):
            files = {"file": open(report_path, "rb")}
            payload = {"payload_json": json.dumps({"embeds": [embed]})}
            response = requests.post(webhook_url, data=payload, files=files)
        else:
            response = requests.post(webhook_url, json={"embeds": [embed]})

        if response.status_code in (200, 204):
            print(f"✅ Discord report sent successfully at {now}")
        else:
            print(f"⚠️ Failed to send Discord message ({response.status_code}): {response.text}")

    except Exception as e:
        print(f"❌ Error sending report: {e}")


if __name__ == "__main__":
    webhook = os.getenv("DISCORD_WEBHOOK_URL", "").strip()
    if webhook:
        send_report(webhook)
    else:
        print("⚠️ No DISCORD_WEBHOOK_URL provided.")
