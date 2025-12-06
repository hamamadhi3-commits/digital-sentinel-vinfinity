import os, json, datetime

MEMORY_PATH = "data/cache/validated/memory_oracle.json"

def load_memory():
    if os.path.exists(MEMORY_PATH):
        with open(MEMORY_PATH, "r") as f:
            return json.load(f)
    return {"memory_log": []}

def save_memory(memory):
    with open(MEMORY_PATH, "w") as f:
        json.dump(memory, f, indent=2)

def update_memory(new_findings):
    memory = load_memory()
    now = datetime.datetime.utcnow().isoformat()
    memory["memory_log"].append({"timestamp": now, "findings": new_findings})
    save_memory(memory)
    print(f"🧬 Memory Oracle updated at {now}")

if __name__ == "__main__":
    # Example usage
    update_memory({"example.com": {"CVE": "2025-0001", "severity": "High"}})
