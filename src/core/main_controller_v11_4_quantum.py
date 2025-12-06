import os
import sys
import json
from datetime import datetime

# Ensure import path includes /src
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# === Core Engines ===
from core.enumeration_engine import run_enumeration
from core.probing_engine import run_probing
from core.crawling_engine import run_crawling
from core.vulnerability_scanner import run_vulnerability_scan
from core.export_bugcrowd import export_bugcrowd
from core.validator import validate_targets
from core.parallel_engine import run_parallel

try:
    from ai.ai_analyzer import analyze_results
    AI_AVAILABLE = True
except ImportError:
    AI_AVAILABLE = False

try:
    from discord_reporter import send_discord_message
    DISCORD_ENABLED = True
except ImportError:
    DISCORD_ENABLED = False


def log_event(stage, message):
    print(f"[{datetime.utcnow().strftime('%H:%M:%S')}] [{stage}] {message}")


def save_report(data, filename="sentinel_report.json"):
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)
    log_event("REPORT", f"Report saved: {filename}")


def main():
    log_event("SYSTEM", "🚀 Sentinel Infinity Engine starting...")

    try:
        targets = validate_targets()
        log_event("VALIDATION", f"✅ {len(targets)} targets validated")

        enum_data = run_enumeration(targets)
        log_event("ENUMERATION", "✅ Enumeration complete")

        live_hosts = run_probing(enum_data)
        log_event("PROBING", f"✅ {len(live_hosts)} live hosts detected")

        crawled = run_crawling(live_hosts)
        log_event("CRAWLING", "✅ Crawling done")

        vulns = run_vulnerability_scan(crawled)
        log_event("SCANNER", "✅ Vulnerability scan complete")

        aggregated = run_parallel([targets, enum_data, live_hosts, vulns])
        log_event("PARALLEL", "✅ Aggregation finished")

        ai_summary = analyze_results(aggregated) if AI_AVAILABLE else {}
        export_bugcrowd(aggregated)

        save_report({
            "targets": targets,
            "enumerated": enum_data,
            "live": live_hosts,
            "vulnerabilities": vulns,
            "ai_summary": ai_summary,
            "timestamp": datetime.utcnow().isoformat()
        })

        if DISCORD_ENABLED:
            send_discord_message("✅ Digital Sentinel Infinity completed successfully!")

        log_event("SYSTEM", "🎯 Mission complete")

    except Exception as e:
        log_event("ERROR", f"❌ {e}")
        if DISCORD_ENABLED:
            send_discord_message(f"❌ Error: {e}")
        raise


if __name__ == "__main__":
    main()
