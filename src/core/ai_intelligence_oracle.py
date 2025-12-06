import json
import os
from datetime import datetime

def analyze_reports():
    print("🧠 [Phase 8: AI Intelligence Oracle Started]")

    # Paths
    export_path = "data/exports/bugcrowd_export.json"
    report_output = "data/reports/ai_intel_summary.json"

    # Check input existence
    if not os.path.exists(export_path):
        print("⚠️ No export data found. Skipping AI analysis.")
        return

    # Load data
    with open(export_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            print("❌ Failed to parse export JSON.")
            return

    # --- Intelligence Core ---
    high_risk = []
    medium_risk = []
    low_risk = []

    for item in data.get("findings", []):
        sev = item.get("severity", "").lower()
        if "critical" in sev or "high" in sev:
            high_risk.append(item)
        elif "medium" in sev:
            medium_risk.append(item)
        else:
            low_risk.append(item)

    # AI summary output
    summary = {
        "timestamp": datetime.utcnow().isoformat(),
        "total_findings": len(data.get("findings", [])),
        "high_risk_count": len(high_risk),
        "medium_risk_count": len(medium_risk),
        "low_risk_count": len(low_risk),
        "high_risk_targets": [x.get("target") for x in high_risk],
        "ai_assessment": "High attention required!" if len(high_risk) > 0 else "No critical issues detected.",
    }

    # Save JSON report
    os.makedirs(os.path.dirname(report_output), exist_ok=True)
    with open(report_output, "w") as rf:
        json.dump(summary, rf, indent=4)

    print("✅ [Phase 8 Completed: Intelligence Summary Generated]")
    print(f"📄 Report saved to: {report_output}")
    print(f"🧩 AI Summary: {summary['ai_assessment']}")
