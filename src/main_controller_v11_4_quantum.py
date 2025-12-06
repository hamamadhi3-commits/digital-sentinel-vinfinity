# src/main_controller_v11_4_quantum.py
import os
import time
from datetime import datetime
from src.enumeration_engine import run_enumeration
from src.probing_engine import run_probing
from src.crawling_engine import run_crawling
from src.discord_reporter import DiscordReporter
from src.core.intel_feed_generator import generate_intel_feed

# 🧠 NEW AI Intelligence Layers
from src.ai.ai_intel_brain import AIIntelBrain
from src.ai.discord_ai_reporter import DiscordAIReporter


def digital_sentinel_controller():
    print("♾️ Digital Sentinel Quantum Controller initiated.")
    
    # Intelligence feed
    print("🧠 Refreshing intelligence feed (Bug Bounty targets)...")
    try:
        generate_intel_feed()
    except Exception as e:
        print(f"⚠️ [Intel] Failed to refresh targets automatically: {e}")

    # Enumeration
    print("🔎 Starting Enumeration Engine...")
    targets_file = "data/targets.txt"
    if not os.path.exists(targets_file):
        print("❌ No targets file found.")
        return

    with open(targets_file, "r") as f:
        targets = [line.strip() for line in f if line.strip()]

    print(f"📥 Loaded {len(targets)} targets from {targets_file}")
    subdomains = run_enumeration(targets)
    print(f"✅ Enumeration phase complete. Found {len(subdomains)} subdomains.")
    
    # Probing
    print("📡 Running Probing Engine...")
    alive_hosts = run_probing(subdomains)
    print(f"✅ Probing complete — {len(alive_hosts)} live domains active.")
    
    # Crawling
    print("🕷️ Activating Crawling Engine...")
    try:
        crawled_data = run_crawling(alive_hosts)
    except Exception as e:
        print(f"💥 Controller crashed during crawling: {e}")
        crawled_data = []

    # === AI INTELLIGENCE MODULE ===
    print("🧠 AI Intelligence Analysis starting...")
    brain = AIIntelBrain()
    ai = DiscordAIReporter()

    for target in alive_hosts[:10]:  # limit per cycle for efficiency
        fake_report = f"Scan result summary for {target} | {len(crawled_data)} pages analyzed."
        ai_result = brain.analyze_vulnerabilities(fake_report)
        ai.send_ai_report(target, ai_result)

    print("✅ AI Intelligence & Reporting phase complete.")

    # Discord reporting (legacy summary)
    try:
        DiscordReporter().send_message(f"✅ Quantum cycle completed ({len(alive_hosts)} live targets).")
    except Exception as e:
        print(f"⚠️ Discord Reporter Error: {e}")

    print("✅ Quantum Controller completed execution.")


def quantum_infinity_loop():
    cycle = 0
    while True:
        cycle += 1
        print(f"🚀 [Quantum-∞] Cycle start @ {datetime.now()}")
        digital_sentinel_controller()
        print(f"✅ [Quantum-∞] Cycle complete")
        wait_time = 6 * 60 * 60  # 6 hours
        print(f"⏱ Waiting {wait_time/3600:.0f} hours before next evolution cycle ({cycle} total)")
        time.sleep(wait_time)


if __name__ == "__main__":
    print("♾️ Digital Sentinel Quantum Immortal Loop — ACTIVE")
    quantum_infinity_loop()
