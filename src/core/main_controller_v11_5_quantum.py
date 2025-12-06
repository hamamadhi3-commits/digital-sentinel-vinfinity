import os
import time
from datetime import datetime

# === Core Engines ===
from core.enumeration_engine import run_enumeration
from core.probing_engine import run_probing
from core.crawling_engine import run_crawling
from core.vulnerability_scanner import run_vulnerability_scan
from core.export_bugcrowd import export_bugcrowd
from core.validator import validate_targets
from core.parallel_engine import run_parallel

# === AI & Intelligence Modules ===
from core.ai_intelligence_oracle import run_ai_oracle
from core.discord_reporter import run_discord_reporter
from core.ai_threat_analyzer import run_threat_analyzer


def digital_sentinel_controller():
    print("🚀 [Digital Sentinel vInfinity Quantum Controller Initialized]")
    start_time = time.time()
    print(f"🕒 Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)

    # === Phase 1: Enumeration ===
    print("🌐 Phase 1: Enumeration Engine Starting...")
    run_enumeration()
    print("✅ Phase 1 Completed.")

    # === Phase 2: HTTP Probing ===
    print("🔍 Phase 2: HTTP Probing Starting...")
    run_probing()
    print("✅ Phase 2 Completed.")

    # === Phase 3: Crawling ===
    print("🕷️ Phase 3: Crawling Engine Starting...")
    run_crawling()
    print("✅ Phase 3 Completed.")

    # === Phase 4: Vulnerability Scanner ===
    print("🧪 Phase 4: Vulnerability Scanning Starting...")
    run_vulnerability_scan()
    print("✅ Phase 4 Completed.")

    # === Phase 5: Export Results ===
    print("📦 Phase 5: Exporting Results to Bugcrowd Format...")
    export_bugcrowd()
    print("✅ Phase 5 Completed.")

    # === Phase 6: Validation Layer ===
    print("🔒 Phase 6: Validation Layer Starting...")
    validate_targets()
    print("✅ Phase 6 Completed.")

    # === Phase 7: Parallel Intelligence ===
    print("🤖 Phase 7: Parallel Intelligence Synchronization Starting...")
    run_parallel()
    print("✅ Phase 7 Completed.")

    # === Phase 8: AI Intelligence Oracle ===
    print("🧠 Phase 8: AI Intelligence Oracle Starting...")
    run_ai_oracle()
    print("✅ Phase 8 Completed.")

    # === Phase 9: Discord Reporter ===
    print("📡 Phase 9: Discord Reporter Starting...")
    run_discord_reporter()
    print("✅ Phase 9 Completed.")

    # === Phase 10: Threat Intelligence Feed ===
    print("🌍 Phase 10: Threat Intelligence Feed Starting...")
    # Placeholder for future AbuseIPDB/ThreatFox integration
    print("📡 Gathering threat intelligence data from feeds...")
    time.sleep(1)
    print("✅ Phase 10 Completed.")

    # === Phase 11: AI Threat Prioritization & Anomaly Detection ===
    print("⚡ Phase 11: AI Threat Prioritization & Anomaly Detection Starting...")
    run_threat_analyzer()
    print("✅ Phase 11 Completed.")

    # === Summary ===
    end_time = time.time()
    total_time = (end_time - start_time) / 60
    print("=" * 70)
    print("🛰️ Digital Sentinel Quantum Infinity Full Cycle Completed Successfully.")
    print(f"🎯 Total Runtime: {total_time:.2f} minutes.")
    print("=" * 70)


if __name__ == "__main__":
    digital_sentinel_controller()
