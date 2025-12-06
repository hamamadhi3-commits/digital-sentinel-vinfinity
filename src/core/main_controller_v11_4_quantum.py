"""
Digital Sentinel - Quantum Infinity Controller v11.4
====================================================
Core orchestration layer of the Sentinel system.
This script coordinates all scanning phases:
1. Enumeration
2. Probing
3. Crawling
4. Vulnerability Scanning
5. Validation
6. Bugcrowd Export
7. Parallel Intelligence Sync
"""

import os
import sys
import time
from datetime import datetime

# ✅ Correct imports after moving modules inside /core
from core.enumeration_engine import run_enumeration
from core.probing_engine import run_probing
from core.crawling_engine import run_crawling
from core.vulnerability_scanner import run_vulnerability_scan
from core.export_bugcrowd import export_bugcrowd
from core.validator import validate_targets
from core.parallel_engine import run_parallel


# ==============================================================
# GLOBAL PATHS & CONFIGURATION
# ==============================================================

ROOT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
DATA_PATH = os.path.join(ROOT_PATH, "data")
TARGETS_FILE = os.path.join(DATA_PATH, "targets.txt")

print("🌐 [Quantum Infinity Controller v11.4]")
print("📁 Working Directory:", ROOT_PATH)
print("🧠 Starting Autonomous Pipeline...\n")


# ==============================================================
# EXECUTION PIPELINE
# ==============================================================

def main():
    start_time = datetime.now()

    try:
        # 1️⃣ ENUMERATION PHASE
        print("🚀 Phase 1: Enumeration Engine Starting...")
        run_enumeration(TARGETS_FILE)
        print("✅ Phase 1 Completed.\n")

        # 2️⃣ PROBING PHASE
        print("🔎 Phase 2: HTTP Probing in Progress...")
        run_probing()
        print("✅ Phase 2 Completed.\n")

        # 3️⃣ CRAWLING PHASE
        print("🕸️ Phase 3: Web Crawling Initiated...")
        run_crawling()
        print("✅ Phase 3 Completed.\n")

        # 4️⃣ SCANNING PHASE
        print("💣 Phase 4: Vulnerability Scanning Executing...")
        run_vulnerability_scan()
        print("✅ Phase 4 Completed.\n")

        # 5️⃣ VALIDATION PHASE
        print("🧩 Phase 5: Validating Discovered Assets...")
        validate_targets()
        print("✅ Phase 5 Completed.\n")

        # 6️⃣ EXPORT PHASE
        print("📤 Phase 6: Exporting Results to Bugcrowd Format...")
        export_bugcrowd()
        print("✅ Phase 6 Completed.\n")

        # 7️⃣ PARALLEL INTELLIGENCE SYNC
        print("🤖 Phase 7: Parallel Intelligence Synchronization...")
        run_parallel()
        print("✅ Phase 7 Completed.\n")

        end_time = datetime.now()
        total = (end_time - start_time).total_seconds() / 60.0
        print(f"🎯 Digital Sentinel Quantum Infinity completed in {total:.2f} minutes.")

    except Exception as e:
        print("❌ FATAL ERROR OCCURRED!")
        print(e)
        sys.exit(1)


if __name__ == "__main__":
    main()
