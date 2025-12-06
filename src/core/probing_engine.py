"""
Digital Sentinel - HTTP Probing Engine
======================================
Checks which targets are alive by probing HTTP/HTTPS responses.
"""

import os
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

# ✅ Ensure output directories exist
SRC_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
DATA_PATH = os.path.join(SRC_PATH, "data")
TARGETS_FILE = os.path.join(DATA_PATH, "targets.txt")
OUTPUT_DIR = os.path.join(DATA_PATH, "cache", "validated")
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "alive_hosts.txt")


def probe_url(domain: str, timeout: int = 5) -> bool:
    """Try to connect via HTTP or HTTPS and check if site is alive."""
    try:
        resp = requests.get(f"http://{domain}", timeout=timeout)
        if resp.status_code < 400:
            return True
    except Exception:
        pass
    try:
        resp = requests.get(f"https://{domain}", timeout=timeout, verify=False)
        return resp.status_code < 400
    except Exception:
        return False


def run_probing():
    """Main orchestrator function — called from main_controller."""
    print("🚀 [Phase 2: HTTP Probing Started]")

    if not os.path.exists(TARGETS_FILE):
        print(f"⚠️ Target list not found at {TARGETS_FILE}")
        return

    with open(TARGETS_FILE, "r") as f:
        targets = [t.strip() for t in f if t.strip()]

    if not targets:
        print("⚠️ No targets found in file.")
        return

    alive = []
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    with ThreadPoolExecutor(max_workers=50) as executor:
        futures = {executor.submit(probe_url, t): t for t in targets}
        for future in as_completed(futures):
            t = futures[future]
            try:
                if future.result():
                    print(f"✅ Alive: {t}")
                    alive.append(t)
                else:
                    print(f"❌ Dead: {t}")
            except Exception as e:
                print(f"⚠️ Error probing {t}: {e}")

    # ✅ Save alive targets
    with open(OUTPUT_FILE, "w") as out:
        out.write("\n".join(alive))

    print(f"\n💾 {len(alive)} alive hosts saved to {OUTPUT_FILE}")
    print("🔚 [Phase 2: HTTP Probing Completed]\n")


# 👇 make sure this exists to allow import
if __name__ == "__main__":
    run_probing()
