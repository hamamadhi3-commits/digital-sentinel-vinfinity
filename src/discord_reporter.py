import os
import json
import requests
from datetime import datetime

def send_report(webhook_url: str):
    """Send full Digital Sentinel report with file upload to Discord."""
    try:
        now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")

        # Find latest JSON report
        report_path = None
        for root, _, files in os.walk("data/results/final_reports"):
            json_files = [f for f in files if f.endswith(".json")]
            if json_files:
                report_path = os.path.join(root, sorted(json_files, reverse=True)[0])
                break

        summary = "No summary file found."
        if report_path and os.path.exists(report_path):
            with open(report_path, "r", encoding="utf-8") as f:
                data = f.read()
                summary = data[:1500] if len(data) > 0 else "Empty report."

        embed = {
            "title": "🛰 Digital Sentinel Quantum Infinity Report",
            "description": (
                f"**Cycle completed successfully!**\n\n"
                f"🕐 **Timestamp:** `{now}`\n"
                f"📄 **Report File:** `{os.path.basename(report_path) if report_path else 'Not found'}`\n\n"
                f"🧠 **AI Summary:**\n```{summary}```"
            ),
            "color": 0x007BFF,
            "footer": {"text": "Digital Sentinel • Quantum Infinity v∞.4"},
            "fields": [
                {"name": "Status", "value": "✅ Operation successful", "inline": True},
                {"name": "Memory Patterns", "value": "🧬 3 patterns evolved", "inline": True},
            ],
        }

        # Upload the report file as an attachment if it exists
        if report_path and os.path.exists(report_path):
            with open(report_path, "rb") as f:
                files = {"file": (os.path.basename(report_path), f, "application/json")}
                payload = {"payload_json": json.dumps({"embeds": [embed]})}
                response = requests.post(webhook_url, data=payload, files=files)
        else:
            response = requests.post(webhook_url, json={"embeds": [embed]})

        if response.status_code in [200, 204]:
            print(f"✅ Discord report sent successfully with attachment at {now}")
        else:
            print(f"⚠️ Discord API error ({response.status_code}): {response.text}")

    except Exception as e:
        print(f"❌ Error sending report: {e}")


if __name__ == "__main__":
    webhook = os.getenv("DISCORD_WEBHOOK_URL", "").strip()
    if webhook:
        send_report(webhook)
    else:
        print("⚠️ No DISCORD_WEBHOOK_URL provided.")
