#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Digital Sentinel — Quantum Controller v11.4
Main orchestration layer controlling all scanning cores (Enumeration, Probing, Crawling, Reporting)
"""

import os
import sys
import time
import traceback
from datetime import datetime

# === Import system engines ===
from src.core.intel_feed_generator import generate_intel_feed
from src.enumeration_engine import run_enumeration
from src.probing_engine import run_probing
from src.crawling_engine import run_crawling
from src.discord_reporter import send_discord_report


# === Global constants ===
DATA_DIR = "data"
RESULTS_DIR = os.path.join(DATA_DIR, "results")
FINAL_REPORTS = os.path.join(RESULTS_DIR, "final_reports")
os.makedirs(FINAL_REPORTS, exist_ok=True)

INTEL_FILE = os.path.join(DATA_DIR, "targets.txt")
LOG_FILE = os.path.join(RESULTS_DIR, "controller.log")


# === Helper: logging ===
def log_event(message: str):
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {message}\n")
    print(message)


# === Core process ===
def digital_sentinel_controller():
    """Main control loop for Quantum Sentinel"""
    log_event("♾️ Digital Sentinel Quantum Controller initiated.")

    try:
        # ====== 1. Refresh Intelligence Feed ======
        log_event("🧠 Refreshing intelligence feed (Bug Bounty targets)...")
        try:
            generate_intel_feed(INTEL_FILE)
            log_event(f"🧩 Intelligence feed updated → {INTEL_FILE}")
        except Exception as e:
            log_event(f"⚠️ [Intel] Failed to refresh targets automatically: {e}")

        # ====== 2. Enumeration Phase ======
        log_event("🔎 Starting Enumeration Engine...")
        subdomains = run_enumeration(INTEL_FILE)

        # ====== 3. Probing Phase ======
        log_event("📡 Running Probing Engine...")
        alive_hosts = run_probing(subdomains)

        # ====== 4. Crawling Phase ======
        log_event("🕷️ Activating Crawling Engine...")
        crawled_data = run_crawling(alive_hosts)

        # ====== 5. Generate Final Report ======
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        final_report = os.path.join(FINAL_REPORTS, f"report_{timestamp}.json")

        import json
        combined_report = {
            "timestamp": timestamp,
            "targets": len(subdomains),
            "alive_hosts": len(alive_hosts),
            "crawled_hosts": len(crawled_data),
            "crawled_data": crawled_data
        }
        with open(final_report, "w", encoding="utf-8") as f:
            json.dump(combined_report, f, indent=2)

        log_event(f"💾 Final Report saved → {final_report}")

        # ====== 6. Discord Notification ======
        summary = (
            f"🕓 Scan Time: {timestamp}\n"
            f"🌐 Targets: {len(subdomains)}\n"
            f"✅ Alive: {len(alive_hosts)}\n"
            f"🕷️ Crawled: {len(crawled_data)}\n"
            f"📄 Report File: {os.path.basename(final_report)}"
        )
        send_discord_report(final_report, summary)
        log_event("📨 Discord report dispatched successfully.")

    except Exception as e:
        log_event(f"💥 Controller crashed: {e}")
        traceback.print_exc()
    finally:
        log_event("✅ Quantum Controller completed execution.")


# === Quantum Immortal Loop (auto-repeat) ===
def quantum_immortal_loop(cycles: int = 9999):
    """Run continuous scanning cycles (auto evolution)."""
    log_event("♾️ Digital Sentinel Quantum Immortal Loop — ACTIVE")

    for i in range(1, cycles + 1):
        start_time = datetime.utcnow()
        log_event(f"🚀 [Quantum-∞] Cycle start @ {start_time}")
        try:
            digital_sentinel_controller()
        except Exception as e:
            log_event(f"❌ Error during cycle {i}: {e}")
        end_time = datetime.utcnow()
        log_event(f"✅ [Quantum-∞] Cycle complete")
        wait_time = (i * 7) % 60 + 10  # random-ish adaptive sleep
        log_event(f"⏱ Waiting {wait_time}s before next evolution cycle ({i} total)")
        time.sleep(wait_time)


# === Entry Point ===
if __name__ == "__main__":
    try:
        core = sys.argv[0]
        print(f"🚀 Running core: {core}")
        quantum_immortal_loop()
    except KeyboardInterrupt:
        log_event("🛑 Manual termination detected.")
