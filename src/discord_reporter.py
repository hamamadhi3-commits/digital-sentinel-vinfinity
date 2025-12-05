import requests
import json

class DiscordReporter:
    def __init__(self, webhook_url):
        self.webhook_url = webhook_url

    def send_embed(self, report_file, submissions):
        embed = {
            "username": "Digital Sentinel • Quantum Infinity v∞.5",
            "embeds": [
                {
                    "title": "🧩 Bugcrowd Report Template Ready",
                    "description": "Cycle validated successfully. Copy these fields into your Bugcrowd submission form.",
                    "color": 5814783,
                    "fields": [
                        {"name": "📁 Report File", "value": report_file, "inline": False},
                        {"name": "🧠 Reports Ready", "value": str(len(submissions)), "inline": True},
                        {"name": "⚙️ Validator", "value": "Active", "inline": True}
                    ],
                    "footer": {"text": "Digital Sentinel • Quantum Infinity v∞.6"},
                }
            ]
        }

        data = json.dumps(embed)
        try:
            res = requests.post(self.webhook_url, headers={"Content-Type": "application/json"}, data=data)
            print("✅ Discord notification sent:", res.status_code)
        except Exception as e:
            print("❌ Discord notification failed:", str(e))
