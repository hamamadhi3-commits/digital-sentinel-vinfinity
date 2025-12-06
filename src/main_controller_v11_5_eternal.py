import os
import time
import json
from datetime import datetime
from src.enumeration_engine import run_enumeration
from src.probing_engine import run_probing
from src.crawling_engine import run_crawling
from src.core.intel_feed_generator import generate_intel_feed

# ==================================================
# ⚙️ Quantum Eternal Controller (24h Autonomous Mode)
# ==================================================

def ensure_targets_file():
    """If targets.txt is empty or missing, fill it with default bug bounty targets."""
    targets_path = "data/targets.txt"
    os.makedirs("data", exist_ok=True)

    default_targets = [
        "paypal.com", "spotify.com", "adobe.com", "bugcrowd.com",
        "google.com", "apple.com", "amazon.com", "dropbox.com",
        "hackerone.com", "tesla.com", "intel.com", "microsoft.com",
        "yeswehack.com", "meta.com", "netflix.com", "airbnb.com",
        "zoom.us", "slack.com", "cloudflare.com", "openai.com"
    ]

    if not os.path.exists(targets_path) or os.path.getsize(targets_path) == 0:
        print("🧠 [Intel] No targets found — generating default intelligence feed...")
        with open(targets_path, "w") as f:
            f.write("\n".join(default_targets))
        print(f"✅ Default targets added ({len(default_targets)} companies).")
    else:
        print("📡 [Intel] Existing targets loaded.")


def digital_sentinel_controller():
    """Main orchestrator for the entire scanning process."""
    print("♾️ Digital Sentinel Quantum Eternal — ACTIVE")
    start_time = datetime.now()

    ensure_targets_file()

    # 1. Refresh intelligence feed
    try:
        print("🧠 Refreshing intelligence feed...")
        generate_intel_feed()
    except Exception as e:
        print(f"⚠️ [Intel] Failed to refresh feed: {e}")

    # 2. Enumeration phase
    print("🔍 Running Enumeration Engine...")
    all_subdomains = run_enumeration("data/targets.txt")
    print(f"✅ Enumeration complete → {len(all_subdomains)} subdomains found.")

    # 3. Probing phase
    print("📡 Running Probing Engine...")
    alive_hosts = run_probing(all_subdomains)
    print(f"✅ Probing complete → {len(alive_hosts)} active domains.")

    # 4. Crawling phase
    print("🕷️ Running Crawling Engine...")
    try:
        crawled_data = run_crawling(alive_hosts)
        print(f"✅ Crawling complete → {len(crawled_data)} domains successfully crawled.")
    except Exception as e:
        print(f"💥 [Crawler Error] {e}")
        crawled_data = []

    # 5. Save JSON Report
    os.makedirs("data/reports", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = f"data/reports/report_{timestamp}.json"
    report = {
        "timestamp": timestamp,
        "targets": len(open('data/targets.txt').read().splitlines()),
        "alive_hosts": len(alive_hosts),
        "crawled_hosts": len(crawled_data),
        "crawled_data": crawled_data
    }
    with open(report_path, "w") as f:
        json.dump(report, f, indent=4)

    print(f"📝 Report saved → {report_path}")
    print(f"🕒 Cycle duration: {datetime.now() - start_time}")
    print("✅ Quantum cycle complete.")


def auto_restart():
    """Automatically restart the workflow after GitHub’s 6h limit."""
    print("♻️ [Quantum-∞] Restarting after 6h GitHub limit...")
    time.sleep(10)
    os.system("gh workflow run sentinel-autonomous-vinfinity.yml")


if __name__ == "__main__":
    try:
        digital_sentinel_controller()
    except Exception as e:
        print(f"💥 Fatal error: {e}")
    finally:
        auto_restart()
