# src/ai/ai_intel_brain.py
import os
import json
import openai
from datetime import datetime

# =========================
# 🧠 DIGITAL SENTINEL - AI BRAIN
# =========================

class AIIntelBrain:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("❌ Missing OpenAI API Key (set OPENAI_API_KEY env var).")
        openai.api_key = self.api_key
        self.memory_file = "data/intel_memory.json"
        self.load_memory()

    def load_memory(self):
        """Load or initialize memory for adaptive learning"""
        if os.path.exists(self.memory_file):
            with open(self.memory_file, "r") as f:
                self.memory = json.load(f)
        else:
            self.memory = {"patterns": [], "stats": {"total_scans": 0}}
            os.makedirs(os.path.dirname(self.memory_file), exist_ok=True)
            self.save_memory()

    def save_memory(self):
        with open(self.memory_file, "w") as f:
            json.dump(self.memory, f, indent=4)

    def analyze_vulnerabilities(self, report_text: str):
        """
        Use GPT to analyze vulnerability report and return:
        - Vulnerability summary
        - Risk score
        - CWE/CVSS classifications
        - Recommendations
        """
        prompt = f"""
        You are a cybersecurity AI assistant analyzing vulnerability reports.
        Analyze the following scan data and summarize:
        1. Number of vulnerabilities
        2. Count of high/medium/low severity
        3. Mention CWE or CVSS scores if available
        4. Provide overall AI Risk Score (0-100)
        5. Write 1-2 clear mitigation recommendations.
        \n\nREPORT DATA:\n{report_text}
        """
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=[{"role": "system", "content": "You are a cybersecurity analyst."},
                          {"role": "user", "content": prompt}],
                max_tokens=600,
                temperature=0.3
            )
            output = response.choices[0].message["content"].strip()
            ai_data = {
                "timestamp": str(datetime.utcnow()),
                "summary": output,
                "risk_score": self.extract_risk_score(output),
            }
            self.memory["stats"]["total_scans"] += 1
            self.memory["patterns"].append(ai_data)
            self.save_memory()
            return ai_data
        except Exception as e:
            return {"error": str(e)}

    def extract_risk_score(self, text: str) -> int:
        """Extract or estimate a risk score from AI output"""
        import re
        match = re.search(r'(\d{1,3})\s*/?\s*100', text)
        if match:
            score = int(match.group(1))
            return min(max(score, 0), 100)
        return 50  # fallback average

# Example standalone usage
if __name__ == "__main__":
    brain = AIIntelBrain()
    test_report = "CVE-2024-1234 found in target.com (CVSS 8.2) SQLi + XSS"
    result = brain.analyze_vulnerabilities(test_report)
    print(result)
