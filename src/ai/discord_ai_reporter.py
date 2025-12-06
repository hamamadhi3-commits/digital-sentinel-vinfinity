# src/ai/discord_ai_reporter.py
import os
import json
import requests

# =========================
# 🔔 DIGITAL SENTINEL - DISCORD AI REPORTER
# =========================

class DiscordAIReporter:
    def __init__(self, webhook_url=None):
        self.webhook_url = webhook_url or os.getenv("DISCORD_WEBHOOK_URL")
        if not self.webhook_url:
            raise ValueError("❌ Missing DISCORD_WEBHOOK_URL environment variable")

    def send_ai_report(self, target, ai_data):
        """Send summarized AI vulnerability report to Discord"""
        embed = {
            "title": f"🧠 Digital Sentinel AI Report — {target}",
            "color": 0xFF4C4C if ai_data.get("risk_score", 50) > 70 else 0x00FF7F,
            "fields": [
                {"name": "🕒 Timestamp", "value": ai_data.get("timestamp", "N/A"), "inline": False},
                {"name": "📊 AI Risk Score", "value": str(ai_data.get("risk_score", "N/A")), "inline": True},
                {"name": "🧩 Summary", "value": ai_data.get("summary", "No summary"), "inline": False},
            ],
            "footer": {"text": "Digital Sentinel vInfinity • Adaptive Intelligence Engine"}
        }

        payload = {"embeds": [embed]}
        try:
            response = requests.post(self.webhook_url, json=payload)
            if response.status_code == 204:
                print(f"✅ Sent AI report to Discord: {target}")
            else:
                print(f"⚠️ Discord response: {response.status_code} → {response.text}")
        except Exception as e:
            print(f"❌ Discord send error: {e}")

# Example standalone usage
if __name__ == "__main__":
    reporter = DiscordAIReporter()
    example_data = {
        "timestamp": "2025-12-05T12:34:56Z",
        "risk_score": 85,
        "summary": "High CVSS SQL Injection found in /login. Patch immediately."
    }
    reporter.send_ai_report("paypal.com", example_data)
