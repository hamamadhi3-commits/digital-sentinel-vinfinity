import json
from datetime import datetime
import os

class BugcrowdExporter:
    def __init__(self, validated_path):
        self.validated_path = validated_path

    def generate_submission(self, issue):
        template = {
            "summary_title": f"{issue.get('signature', '').upper()} vulnerability on {issue.get('url', 'unknown')}",
            "target": issue.get("url", "unknown"),
            "vrt_category": issue.get("signature", "General Vulnerability"),
            "vulnerability_type": issue.get("signature", "General"),
            "url": issue.get("url", "N/A"),
            "description": f"{issue.get('signature', '').upper()} vulnerability detected and validated.\n"
                           f"Payload confirmed active. See attached report.\n\n"
                           f"Validation timestamp: {issue.get('validated_timestamp', 'N/A')}",
            "attachments": [os.path.basename(self.validated_path)]
        }
        return template

    def export_all(self):
        with open(self.validated_path, "r") as f:
            validated_data = json.load(f)

        submissions = [self.generate_submission(i) for i in validated_data if i.get("validated")]
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        output_path = f"data/results/bugcrowd_exports/export_{timestamp}.json"

        with open(output_path, "w") as f:
            json.dump(submissions, f, indent=2)

        print(f"📦 Bugcrowd export created → {output_path}")
        return output_path
