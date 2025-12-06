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

# === AI Intelligence Modules ===
from core.ai_intelligence_oracle import analyze_reports


def digital_sentinel_controller():
    print("🚀 [Digital Sentinel vInfinity Quantum Controller Initialized]")
    start_time = time.time()
    print(f"🕒 Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)

    # === Phase 1: Subdomain Enumeration ===
    print("\n🌐 Phase 1: Enumeration Engine Starting...")
    run_enumeration()
    print("✅ Phase 1 Completed.")

    # === Phase 2: HTTP Probing ===
    print("\n🔍 Phase 2: HTTP Probing Starting...")
    run_probing()
    print("✅ Phase 2 Completed.")

    # === Phase 3: Crawling Engine ===
    print("\n🕷️ Phase 3: Crawling Engine Starting...")
    run_crawling()
    print("✅ Phase 3 Completed.")

    # === Phase 4: Vulnerability Scanning ===
    print("\n🧪 Phase 4: Vulnerability Scanning Starting...")
    run_vulnerability_scan()
    print("✅ Phase 4 Completed.")

    # === Phase 5: Export Bugcrowd Format ===
    print("\n📦 Phase 5: Exporting Results to Bugcrowd Format...")
    export_bugcrowd()
    print("✅ Phase 5 Completed.")

    # === Phase 6: Validation Layer ===
    print("\n🔒 Phase 6: Validation Layer Starting...")
    validate_targets()
    print("✅ Phase 6 Completed.")

    # === Phase 7: Parallel Intelligence Synchronization ===
    print("\n🤖 Phase 7: Parallel Intelligence Synchronization Starting...")
    run_parallel()
    print("✅ Phase 7 Completed.")

    # === Phase 8: AI Intelligence Oracle ===
    print("\n🧠 Phase 8: AI Intelligence Oracle Starting...")
    analyze_reports()
    print("✅ Phase 8 Completed.")
    print("🎯 Digital Sentinel Quantum Infinity AI Layer Operational.")

    # === Wrap-up ===
    end_time = time.time()
    duration = (end_time - start_time) / 60
    print("=" * 70)
    print(f"🎯 Digital Sentinel Quantum Infinity completed in {duration:.2f} minutes.")
    print("=" * 70)


if __name__ == "__main__":
    digital_sentinel_controller()
