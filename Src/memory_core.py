import json, os

def evolve_learning(data):
    os.makedirs("data/memory", exist_ok=True)
    path = "data/memory/learning.json"
    if os.path.exists(path):
        with open(path, "r") as f:
            memory = json.load(f)
    else:
        memory = {}
    for sig in data.get("signatures", []):
        memory[sig] = memory.get(sig, 0) + 1
    with open(path, "w") as f:
        json.dump(memory, f, indent=2)
    print(f"🧬 Memory evolved — {len(memory)} patterns stored.")
