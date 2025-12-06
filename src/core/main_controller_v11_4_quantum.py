import os
import time
import json
from datetime import datetime

# === Core Engines ===
from core.enumeration_engine import run_enumeration
from core.probing_engine import run_probing
from core.crawling_engine import run_crawling
from core.vulnerability_scanner import run_vulnerability_scan
from core.export_bugcrowd import export_results
from core.validator import validate_results
from core.parallel_engine import run_parallel_tasks


# === Digital Sentinel | Quantum Controller v11.4 ===
class QuantumSentinelController:
    def __init__(self):
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.report_dir = f"reports/{self.session_id}"
        os.makedirs(self.report_dir, exist_ok=True)

        self.metadata = {
            "session_id": self.session_id,
            "timestamp": datetime.now().isoformat(),
            "version": "11.4",
            "status": "initialized"
        }

    def log(self, message: str):
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] {message}")

    def save_metadata(self):
        meta_path = os.path.join(self.report_dir, "metadata.json")
        with open(meta_path, "w") as f:
            json.dump(self.metadata, f, indent=2)
        self.log(f"Metadata saved → {meta_path}")

    def execute_pipeline(self):
        self.log("🚀 Starting Digital Sentinel Infinity Pipeline")

        try:
            # === Phase 1: Enumeration ===
            self.log("🔍 Running Enumeration Engine...")
            enum_results = run_enumeration()
            self.log(f"Enumeration completed → {len(enum_results)} hosts discovered")

            # === Phase 2: HTTP Probing ===
            self.log("🌐 Running Probing Engine...")
            probed = run_probing(enum_results)
            self.log(f"Active targets found → {len(probed)}")

            # === Phase 3: Crawling ===
            self.log("🕷️ Running Crawling Engine...")
            crawled_data = run_crawling(probed)
            self.log("Crawling completed successfully")

            # === Phase 4: Vulnerability Scanning ===
            self.log("🧠 Running Vulnerability Scanner...")
            vuln_results = run_vulnerability_scan(crawled_data)
            self.log(f"Potential findings: {len(vuln_results)}")

            # === Phase 5: Validation ===
            self.log("🧩 Validating results...")
            validated = validate_results(vuln_results)
            self.log(f"Validated findings: {len(validated)}")

            # === Phase 6: Parallel Processing (AI-based analysis, tagging, reporting) ===
            self.log("⚙️ Running Parallel AI Analysis...")
            run_parallel_tasks(validated)
            self.log("Parallel AI analysis complete")

            # === Phase 7: Export Reports ===
            self.log("📦 Exporting results to Bugcrowd/Output channel...")
            export_results(validated, output_dir=self.report_dir)

            # === Finalize ===
            self.metadata["status"] = "completed"
            self.save_metadata()
            self.log("✅ Digital Sentinel Infinity cycle completed successfully.")

        except Exception as e:
            self.metadata["status"] = "failed"
            self.metadata["error"] = str(e)
            self.save_metadata()
            self.log(f"❌ Fatal error: {e}")


if __name__ == "__main__":
    controller = QuantumSentinelController()
    controller.execute_pipeline()
