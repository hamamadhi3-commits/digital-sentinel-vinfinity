from core.enumeration_engine import run_enumeration
from core.probing_engine import run_probing
from core.crawling_engine import run_crawling
from core.vulnerability_scanner import run_vulnerability_scan
from core.export_bugcrowd import export_bugcrowd
from core.validator import validate_targets
from core.parallel_engine import run_parallel
from core.ai_intelligence_oracle import run_ai_oracle
from core.discord_reporter import send_discord_report
from core.threat_intel_feed import run_threat_feed
import datetime, os

print("🚀 [Digital Sentinel vInfinity Quantum Controller Initialized]")
print(f"🕒 Start Time: {datetime.datetime.now()}")

# === Phase 1–9 ===
run_enumeration()
run_probing()
run_crawling()
run_vulnerability_scan()
export_bugcrowd()
validate_targets()
run_parallel()
run_ai_oracle()
send_discord_report()

# === Phase 10 ===
print("🌍 Phase 10: Threat Intelligence Integration Starting...")
run_threat_feed()
print("✅ Phase 10 Completed.")

print("=====================================================================")
print("🛰️ Digital Sentinel Quantum Infinity Threat-Aware Mode Active.")
print("=====================================================================")
