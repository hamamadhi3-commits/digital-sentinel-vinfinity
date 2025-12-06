"""
Digital Sentinel - Export Bugcrowd
==================================
Simulates exporting vulnerability results to Bugcrowd-compatible format.
"""

import os
import json
import time

def export_bugcrowd():
    """Simulated export to Bugcrowd format."""
    print("🚀 [Phase 5: Export Bugcrowd Started]")

    input_file = os.path.join("data", "cache", "vulnerabilities", "scan_report.txt")
    output_dir = os.path.join("data", "exports")
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, "bugcrowd_export.json")

    if not os.path.exists(input_file):
        print(f"⚠️ Vulnerability scan report not found at {input_file}")
        return

    with open(input_file, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    data = []
    for idx, line in enumerate(lines, start=1):
        severity = "info"
        if "[HIGH]" in line:
            severity = "high"
        elif "[MEDIUM]" in line:
            severity = "medium"
        data.append({
            "id": idx,
            "severity": severity,
            "description": line,
            "status": "open"
        })

    with open(output_file, "w") as f:
        json.dump({"findings": data}, f, indent=4)

    time.sleep(1)
    print(f"💾 Bugcrowd-compatible export created at {output_file}")
    print("🔚 [Phase 5: Export Completed]")


if __name__ == "__main__":
    export_bugcrowd()
