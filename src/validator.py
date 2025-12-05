import requests
import json
from datetime import datetime
from urllib.parse import urljoin

class AutoValidator:
    def __init__(self, report_path="data/results/final_reports/report_latest.json"):
        self.report_path = report_path
        self.validated_issues = []
        self.payloads = {
            "xss": "<script>alert('DigitalSentinel')</script>",
            "sqli": "' OR '1'='1",
            "csrf": "<form action='/submit' method='POST'><input type='hidden' name='csrf_test' value='1'></form>"
        }

    def load_report(self):
        with open(self.report_path, "r") as f:
            data = json.load(f)
        return data

    def validate_issue(self, issue):
        vuln_type = issue.get("signature", "").lower()
        url = issue.get("url")
        payload = self.payloads.get(vuln_type)
        if not payload or not url:
            return None

        try:
            response = requests.get(url, params={"test": payload}, timeout=6)
            if payload in response.text or response.status_code == 500:
                issue["validated"] = True
                issue["validated_timestamp"] = datetime.utcnow().isoformat()
                print(f"[✅ VALID] {vuln_type.upper()} confirmed at {url}")
            else:
                issue["validated"] = False
        except Exception as e:
            issue["validated"] = False
            issue["error"] = str(e)

        return issue

    def run(self):
        print("🧪 Running Auto-Validation module...")
        report = self.load_report()
        for issue in report.get("issues", []):
            validated = self.validate_issue(issue)
            if validated:
                self.validated_issues.append(validated)

        output_path = f"data/cache/validated/validated_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.json"
        with open(output_path, "w") as f:
            json.dump(self.validated_issues, f, indent=2)
        print(f"💾 Validation results saved → {output_path}")
        return output_path
