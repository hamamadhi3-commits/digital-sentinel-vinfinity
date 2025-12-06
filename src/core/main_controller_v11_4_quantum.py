import os
import sys
import time
import json
from datetime import datetime

# === Ensure imports work ===
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# === Core Engines ===
from core.enumeration_engine import run_enumeration
from core.probing_engine import run_probing
from core.crawling_engine import run_crawling
from core.vulnerability_scanner import run_vulnerability_scan
from core.export_bugcrowd import export_bugcrowd
from core.validator import validate_targets
from core.parallel_engine import run_parallel

# === Optional AI Module ===
try:
    from ai.ai_analyzer import analyze_results
    AI_AVAILABLE = True
except ImportError:
    AI_AVAILABLE = False

# === Optional Discord Reporter ===
try:
    from discord_reporter import send_discord_message
    DISCORD_ENABLED = True
except ImportError:
    DISCORD_ENABLED = False


def log_event(stage: str, status: str):
    """Logs stages with timestamps"""
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    message = f"[{timestamp}] [{stage.upper()}] ➤ {status}"
    print(message)
    return message


def save_report(data, filename="sentinel_report.json"):
    """Save final report to local file"""
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)
    log_event("REPORT", f"Saved report → {filename}")


def main():
    log_event("SYSTEM", "🚀 Digital Sentinel Infinity Engine initialized...")

    try:
        # === Stage 1: Validate Targets ===
        log_event("VALIDATION", "🔍 Validating targets...")
        validated_targets = validate_targets()
        log_event("VALIDATION", f"✅ {len(validated_targets)} targets ready")

        # === Stage 2: Enumeration ===
        log_event("ENUMERATION", "🌐 Running enumeration...")
        enumerated = run_enumeration(validated_targets)
        log_event("ENUMERATION", "✅ Enumeration complete")

        # === Stage 3: Probing ===
        log_event("PROBING", "📡 Probing live hosts...")
        live_hosts = run_probing(enumerated)
        log_event("PROBING", f"✅ Found {len(live_hosts)} live hosts")

        # === Stage 4: Crawling ===
        log_event("CRAWLING", "🕷️ Crawling targets...")
        crawled = run_crawling(live_hosts)
        log_event("CRAWLING", "✅ Crawling complete")

        # === Stage 5: Vulnerability Scanning ===
        log_event("SCANNER", "🧠 Scanning for vulnerabilities...")
        vuln_results = run_vulnerability_scan(crawled)
        log_event("SCANNER", "✅ Vulnerability scanning complete")

        # === Stage 6: Parallel Aggregation ===
        log_event("PARALLEL", "⚙️ Aggregating results in parallel...")
        aggregated = run_parallel([validated_targets, enumerated, live_hosts, vuln_results])
        log_event("PARALLEL", "✅ Aggregation done")

        # === Stage 7: AI Analysis (if available) ===
        if AI_AVAILABLE:
            log_event("AI", "🤖 Performing AI-driven analysis...")
            ai_summary = analyze_results(aggregated)
            log_event("AI", "✅ AI analysis complete")
        else:
            ai_summary = {"status": "AI module unavailable"}
            log_event("AI", "⚠️ Skipped AI analysis")

        # === Stage 8: Export ===
        log_event("EXPORT", "📤 Exporting to Bugcrowd format...")
        export_bugcrowd(aggregated)
        log_event("EXPORT", "✅ Export complete")

        # === Stage 9: Save Final Report ===
        final_report = {
            "validated_targets": validated_targets,
            "enumerated": enumerated,
            "live_hosts": live_hosts,
            "vulnerabilities": vuln_results,
            "ai_summary": ai_summary,
            "timestamp": datetime.utcnow().isoformat(),
        }
        save_report(final_report)

        # === Stage 10: Discord Notification ===
        if DISCORD_ENABLED:
            send_discord_message("✅ Digital Sentinel Infinity mission completed.")
        else:
            log_event("DISCORD", "⚠️ Skipped Discord notification")

        log_event("SYSTEM", "🎯 Mission accomplished successfully.")

    except Exception as e:
        err_msg = f"❌ Error: {str(e)}"
        log_event("SYSTEM", err_msg)
        if DISCORD_ENABLED:
            send_discord_message(err_msg)
        raise


if __name__ == "__main__":
    main()
