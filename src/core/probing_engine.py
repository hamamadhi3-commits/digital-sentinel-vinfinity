"""
Digital Sentinel - Probing Engine
=================================
This module handles HTTP probing for all discovered subdomains.
It checks which targets are alive and responsive.
"""

import os
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

# Path to discovered subdomains file
SRC_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
DATA_PATH = os.path.join(SRC_PATH, "data")
TARGETS_FILE = os.path.join(DATA_PATH, "targets.txt")
OUTPUT_FILE = os.path.join(DATA_PATH, "cache", "validated", "alive_hosts.txt")


def probe_url(url: str, timeout: int = 5) -> bool:
    """Send a GET request to see if a domain is alive."""
    try:
        r = requests.get(f"http://{url}", timeout=timeout)
        if r.status_code < 400:
            return True
        # try https if http fails
        r = requests.get(f"https://{url}", timeout=timeout, verify=False)
        return r.status_code < 400
    except Exception:
        return False


def run_probing():
    """Main function to run HTTP probing on all discovered targets."""
    print("🔎 [Phase 2: HTTP Probing Engine Started]")
    
    if not os.path.exists(TARGETS_FILE):
        print(f"⚠️ No targets file found at {TARGETS_FILE}")
        return

    with open(TARGETS_FILE, "r") as f:
        targets = [line.strip() for line in f if line.strip()]

    if not targets:
        print("⚠️ No targets found to probe.")
        return

    alive_hosts = []
    with ThreadPoolExecutor(max_workers=50) as executor:
        futures = {executor.submit(probe_url, t): t for t in targets}
        for future in as_completed(futures):
            target = futures[future]
            try:
                if future.result():
                    alive_hosts.append(target)
                    print(f"✅ Alive: {target}")
                else:
                    print(f"❌ Dead: {target}")
            except Exception as e:
                print(f"⚠️ Error probing {target}: {e}")

    # Save alive hosts
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, "w") as out:
        out.write("\n".join(alive_hosts))

    print(f"\n💾 Saved {len(alive_hosts)} alive hosts to {OUTPUT_FILE}")
    print("🔚 [Phase 2 Completed - HTTP Probing Engine]\n")
