import os
import time
import json
from datetime import datetime

# === Core Engines ===
from src.core.enumeration_engine import run_enumeration
from src.core.probing_engine import run_probing
from src.core.crawling_engine import run_crawling
from src.core.vulnerability_scanner import run_vulnerability_scan
from src.core.export_bugcrowd import export_to_bugcrowd
from src.core.validator import validate_targets
from src.core.parallel_engine import run_parallel_engine

# === AI & Intelligence Modules ===
from src.ai.ai_auto_triage import analyze_findings, send_to_discord
from src.ai.intel_memory_oracle import update_memory


def digital_sentinel_controller():
    print("🚀 [Digital Sentinel vInfinity Engine] Starting autonomous cycle...")
    start_time = time.time()

    # === 1️⃣ Load and validate targets ===
    targets_file = "data/targets.txt"
    if not os.path.exists(targets_file):
        print("❌ No targets.txt found.")
        return
    validated_targets = validate_targets(targets_file)
    print(f"✅ {len(validated_targets)} targets validated.")

    # === 2️⃣ Enumeration + Probing (Parallel) ===
    print("🕵️ Running parallel enumeration and probing...")
    enumerated_data = run_parallel_engine(validated_targets, run_enumeration)
    probed_data = run_parallel_engine(enumerated_data, run_probing)
    print("✅ Enumeration & probing completed.")

    # === 3️⃣ Crawling + Vulnerability Scanning ===
    print("🧭 Running web crawling and vulnerability scanning...")
    crawled_data = run_parallel_engine(probed_data, run_crawling)
    vulns_data = run_parallel_engine(crawled_data, run_vulnerability_scan)
    print("✅ Crawling and scanning completed.")

    # === 4️⃣ Export results to structured format ===
    export_path = "data/results/final_reports/"
    os.makedirs(export_path, exist_ok=True)
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    report_file = os.path.join(export_path, f"report_{timestamp}.json")

    with open(report_file, "w") as f:
        json.dump(vulns_data, f, indent=2)
    print(f"📦 Results saved to: {report_file}")

    # === 5️⃣ Export to Bugcrowd-compatible format ===
    export_to_bugcrowd(vulns_data)

    # === 6️⃣ AI Auto-Triage (OpenAI GPT integration) ===
    print("🤖 Running AI Auto-Triage & Report Summarization...")
    triage_summaries = analyze_findings()
    if triage_summaries:
        send_to_discord(triage_summaries)
        update_memory(triage_summaries)
        print("🧠 AI triage and memory update complete.")
    else:
        print("⚠️ No findings to triage.")

    # === 7️⃣ Finish Cycle ===
    elapsed = time.time() - start_time
    print(f"🏁 Digital Sentinel cycle completed in {elapsed:.2f}s.")


if __name__ == "__main__":
    try:
        digital_sentinel_controller()
    except Exception as e:
        print("💥 Fatal error in main controller:", str(e))
