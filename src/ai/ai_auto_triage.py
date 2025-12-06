import os, json, requests, openai

def analyze_findings(findings_path="data/results/final_reports/"):
    openai.api_key = os.getenv("OPENAI_API_KEY")
    reports = []
    for file in os.listdir(findings_path):
        if file.endswith(".json"):
            with open(os.path.join(findings_path, file), "r") as f:
                data = json.load(f)
                reports.append(data)

    if not reports:
        print("🚫 No reports found for triage.")
        return None

    summaries = []
    for rep in reports:
        summary_prompt = f"""You are a security analyst. Summarize and classify vulnerabilities by severity (Critical/High/Medium/Low):
        Data: {json.dumps(rep, indent=2)}"""
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=[{"role": "system", "content": "You are a cybersecurity triage AI."},
                          {"role": "user", "content": summary_prompt}]
            )
            ai_summary = response.choices[0].message.content
            summaries.append(ai_summary)
        except Exception as e:
            print("❌ OpenAI triage failed:", e)
    return summaries


def send_to_discord(summaries):
    webhook = os.getenv("DISCORD_WEBHOOK_URL")
    if not webhook:
        print("⚠️ No Discord webhook configured.")
        return
    for s in summaries:
        payload = {"content": f"🧠 **AI-Triage Summary:**\n{s}"}
        requests.post(webhook, json=payload)
    print("✅ AI summaries sent to Discord.")


if __name__ == "__main__":
    result = analyze_findings()
    if result:
        send_to_discord(result)
