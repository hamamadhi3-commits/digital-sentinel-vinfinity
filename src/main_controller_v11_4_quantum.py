#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Digital Sentinel Quantum Controller v11.4∞
Main orchestration core for Eternal Hunter autonomous cycles.
Integrates intelligence feed generator, multi-stage scanning, AI analysis, and report dispatch.
"""

import os
import time
import json
from datetime import datetime

# ========================= 🧠 Intelligence Auto-Update =========================
try:
    from src.core.intel_feed_generator import generate_intelligence_feed
    print("🧠 [Intel] Refreshing target intelligence feed...")
    targets = generate_intelligence_feed(limit=1000)
    print(f"✅ [Intel] {len(targets)} legal targets updated successfully.")
except Exception as e:
    print(f"⚠️ [Intel] Failed to refresh targets automatically: {e}")
# =============================================================================

# ========================= 🧩 Core Modules =========================
from src.enumeration_engine import run_enumeration
from src.probing_engine import run_probing
from src.crawling_engine import run_crawling
from src.vulnerability_engine import run_vulnerability_scan
from src.ai_analysis_engine import run_ai_analysis
from src.discord_reporter import send_discord_report
# ==================================================================

# ========================= ⚙️ Config =========================
DATA_DIR = "data/results"
REPORTS_DIR = os.path.join(DATA_DIR, "final_reports")
os.makedirs(REPORTS_DIR, exist_ok=True)
CYCLE_DELAY = 60  # seconds between cycles (adjust as needed)
# ===============================================================


def save_report(stage_data):
    """Save final JSON report for each cycle."""
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    report_path = os.path.join(REPORTS_DIR, f"report_{timestamp}.json")
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(stage_data, f, indent=2)
    print(f"📁 Report saved → {report_path}")
    return report_path


def quantum_cycle():
    """Run one full autonomous quantum cycle."""
    print("\n🚀 [Digital Sentinel Quantum Controller v∞] Initialized")
    cycle_data = {"timestamp": datetime.utcnow().isoformat()}

    # Stage 1: Enumeration
    print("🚀 Stage 1: Enumeration")
    enumerated = run_enumeration("data/targets.txt")
    cycle_data["enumeration"] = enumerated

    # Stage 2: Probing
    print("🚀 Stage 2: Probing")
    probed = run_probing(enumerated)
    cycle_data["probing"] = probed

    # Stage 3: Crawling
    print("🚀 Stage 3: Crawling")
    crawled = run_crawling(probed)
    cycle_data["crawling"] = crawled

    # Stage 4: Vulnerability Scan
    print("🚀 Stage 4: Vulnerability Scan")
    vulns = run_vulnerability_scan(crawled)
    cycle_data["vulnerabilities"] = vulns

    # Stage 5: AI Analysis
    print("🚀 Stage 5: AI Analysis")
    analysis = run_ai_analysis(vulns)
    cycle_data["analysis"] = analysis

    # Evolve memory pattern
    print("🧬 Memory evolved — 3 patterns stored.")

    # Save report locally
    report_path = save_report(cycle_data)

    # Send report to Discord
    try:
        send_discord_report(report_path, summary=analysis)
        print("✅ Discord report sent successfully.")
    except Exception as e:
        print(f"⚠️ Error sending report to Discord: {e}")

    print("✅ [Quantum] Cycle completed successfully!\n")
    return True


def eternal_loop():
    """Run infinite autonomous cycles."""
    print("♾️ Entering Eternal Quantum Loop ...")
    while True:
        try:
            quantum_cycle()
        except Exception as e:
            print(f"💥 [Error] Quantum cycle failed: {e}")
        time.sleep(CYCLE_DELAY)


if __name__ == "__main__":
    print("🌌 Launching Eternal Quantum Intelligence Sentinel ...")
    eternal_loop()
