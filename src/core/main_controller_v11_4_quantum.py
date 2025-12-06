import os
import sys
import time
import json
from datetime import datetime

# === Fix import paths dynamically ===
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# === Core Engines ===
from src.core.enumeration_engine import run_enumeration
from src.core.probing_engine import run_probing
from src.core.crawling_engine import run_crawling
from src.core.vulnerability_scanner import run_vulnerability_scan
from src.core.export_bugcrowd import export_bugcrowd
from src.core.validator import validate_targets
from src.core.parallel_engine import run_parallel

# === AI Module (Optional) ===
try:
    from src.ai.ai_analyzer import analyze_results
    AI_AVAILABLE = True
except ImportError:
    AI_AVAILABLE = False

# === Reporter ===
try:
    from src.discord_reporter import send_discord_message
    DISCORD_ENABLED = True
except ImportError:
    DISCORD_ENABLED = False


# === Utility ===
def log_event(stage: str, status: str):
    """Prints and logs each stage in a unified way."""
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    message = f"[{timestamp}] [{stage.upper()}] ➤ {status}"
    print(message)
    return message


def save_report(data, filename="sentinel_report.json"):
    """Save the final JSON report locally."""
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)
    log_event("REPORT", f"Saved as {filename}")


# === Main Execution ===
def main():
    log_event("SYSTEM", "🚀 Digital Sentinel Infinity Engine starting...")

    try:
        # === Stage 1: Target Validation ===
        log_event("VALIDATION", "🔍 Validating target list...")
        validated_targets = validate_targets()
        log_event("VALIDATION", f"✅ {len(validated_targets)} targets validated")

        # === Stage 2: Enumeration ===
        log_event("ENUMERATION", "🌐 Enumerating subdomains...")
        enumerated_data = run_enumeration(validated_targets)
        log_event("ENUMERATION", "✅ Enumeration completed")

        # === Stage 3: HTTP Probing ===
        log_event("PROBING", "📡 Probing live hosts...")
        live_hosts = run_probing(enumerated_data)
        log_event("PROBING", f"✅ {len(live_hosts)} live hosts identified")

        # === Stage 4: Crawling ===
        log_event("CRAWLING", "🕷️ Crawling web apps...")
        crawled_data = run_crawling(live_hosts)
        log_event("CRAWLING", "✅ Crawling complete")

        # === Stage 5: Vulnerability Scanning ===
        log_event("SCANNER", "🧠 Running vulnerability scans...")
        vuln_results = run_vulnerability_scan(crawled_data)
        log_event("SCANNER", "✅ Vulnerability scan complete")

        # === Stage 6: Parallel Aggregation ===
        log_event("PARALLEL", "⚙️ Aggregating all modules in parallel...")
        aggregated = run_parallel([validated_targets, enumerated_data, live_hosts, vuln_results])
        log_event("PARALLEL", "✅ Aggregation complete")

        # === Stage 7: AI Analysis (Optional) ===
        if AI_AVAILABLE:
            log_event("AI", "🤖 Running AI analysis on results...")
            ai_summary = analyze_results(aggregated)
            log_event("AI", "✅ AI analysis complete")
        else:
            ai_summary = {"status": "AI module not loaded"}
            log_event("AI", "⚠️ Skipped — AI module not found")

        # === Stage 8: Export ===
        log_event("EXPORT", "📤 Exporting report for Bugcrowd format...")
        export_bugcrowd(aggregated)
        log_event("EXPORT", "✅ Export complete")

        # === Stage 9: Save Final Report ===
        final_report = {
            "validated_targets": validated_targets,
            "enumerated": enumerated_data,
            "live_hosts": live_hosts,
            "vulnerabilities": vuln_results,
            "ai_summary": ai_summary,
            "timestamp": datetime.utcnow().isoformat(),
        }
        save_report(final_report)

        # === Stage 10: Discord Notification ===
        if DISCORD_ENABLED:
            send_discord_message("✅ Digital Sentinel Infinity: mission complete.")
        else:
            log_event("DISCORD", "⚠️ Skipped — Discord module not active")

        log_event("SYSTEM", "🎯 Mission accomplished — all stages complete.")

    except Exception as e:
        error_msg = f"❌ Error: {str(e)}"
        log_event("SYSTEM", error_msg)
        if DISCORD_ENABLED:
            send_discord_message(error_msg)
        raise


# === Entry Point ===
if __name__ == "__main__":
    main()
