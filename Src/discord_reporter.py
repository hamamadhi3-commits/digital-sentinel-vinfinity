import os, json, requests

WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

def send_report(path):
    if not WEBHOOK_URL:
        print("⚠️ No Discord webhook configured.")
        return
    with open(path, "r") as f:
        data = json.load(f)
    embed = {
        "embeds": [{
            "title": f"📡 Digital Sentinel Quantum v∞ Report",
            "description": f"**Domains:** {data['domains_scanned']}\n"
                           f"**URLs:** {data['urls_scanned']}\n"
                           f"**Issues:** {data['issues_found']}\n"
                           f"**AI Findings:** {data['ai_findings']}",
            "color": 0x00FFFF,
            "footer": {"text": "Eternal Quantum Sentinel"}
        }]
    }
    requests.post(WEBHOOK_URL, json=embed)
    print("📨 Discord report sent successfully!")
