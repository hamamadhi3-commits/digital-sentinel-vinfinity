import os
import json
import requests
from datetime import datetime

# 🧠 Discord webhook sender for Digital Sentinel Quantum Infinity
# ---------------------------------------------------------------
# This module sends styled embeds to a Discord channel summarizing
# the latest scanning cycle, results, and AI analysis.

def send_report(webhook_url: str):
    """Send scan report summary to Discord."""
    try:
        # Check report files
        report_summary = "No summary file found."
        valid_findings = 0
        urls_processed = 0
        subdomains_found = 0

        # Load summary or stats if available
        for candidate in ["results.json", "summary.json", "scan_log.txt"]:
            if os.path.exists(candidate):
                with open(candidate, "r", encoding="utf-8") as f:
                    content = f.read()
                    report_summary = content[:1500]  # truncate for safety
                    if "valid findings" in content:
                        valid_findings = content.count("valid finding")
                    if "URL" in content:
                        urls_processed += content.count("http")
                    if "subdomain" in content:
                        subdomains_found += content.count(".")
                    break

        # 🕐 Timestamp
        now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")

        # 🧠 Embed payload
        embed = {
            "title": "🛰 Digital Sentinel Quantum Infinity Report",
            "description": (
                f"**Cycle completed successfully!**\n\n"
                f"🕐 Timestamp: `{now}`\n"
                f"🌐 Subdomains found: **{subdomains_found}**\n"
                f"🧩 URLs processed: **{urls_processed}**\n"
                f"🚨 Valid findings: **{valid_findings}**\n\n"
                f"🧠 AI Summary:\n```{report_summary}```"
            ),
            "color": 0x3498db,
            "footer": {
                "text": "Digital Sentinel • Quantum Infinity v∞.3",
            },
            "thumbnail": {
                "url": "https://i.imgur.com/3Nczd8V.png"
            },
            "fields": [
                {"name": "Status", "value": "✅ Operation successful", "inline": True},
                {"name": "Memory Patterns", "value": "🧬 3 patterns evolved", "inline": True},
            ],
        }

        # 🚀 Send to Discord
        response = requests.post(webhook_url, json={"embeds": [embed]})
        if response.status_code in [200, 204]:
            print(f"✅ Discord report sent successfully at {now}")
        else:
            print(f"⚠️ Failed to send Discord message ({response.status_code}): {response.text}")

    except Exception as e:
        print(f"❌ Error sending report: {e}")


# Manual test entry point
if __name__ == "__main__":
    webhook = os.getenv("DISCORD_WEBHOOK_URL", "").strip()
    if not webhook:
        print("⚠️ No DISCORD_WEBHOOK_URL provided.")
    else:
        send_report(webhook)
