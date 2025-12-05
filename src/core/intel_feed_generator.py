#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Digital Sentinel Intelligence Feed Generator v∞
Auto-fetches 1000+ legal Bug Bounty targets from public programs (HackerOne, Bugcrowd, Intigriti, YesWeHack, Immunefi)
and writes them into data/targets.txt
"""

import requests
import os
import time
from datetime import datetime

TARGETS_FILE = "data/targets.txt"
MAX_TARGETS = 1000

# ---------------------- Helper functions ----------------------

def write_targets(targets):
    """Write collected targets to data/targets.txt"""
    os.makedirs(os.path.dirname(TARGETS_FILE), exist_ok=True)
    with open(TARGETS_FILE, "w", encoding="utf-8") as f:
        for t in sorted(set(targets)):
            f.write(t.strip() + "\n")
    print(f"✅ Saved {len(targets)} unique targets → {TARGETS_FILE}")

def fetch_json(url):
    """Fetch JSON safely with retries"""
    for _ in range(3):
        try:
            r = requests.get(url, timeout=10)
            if r.status_code == 200:
                return r.json()
        except Exception:
            time.sleep(2)
    return {}

# ---------------------- HackerOne ----------------------

def fetch_hackerone_targets(limit=200):
    print("🧠 Fetching HackerOne programs...")
    url = "https://raw.githubusercontent.com/projectdiscovery/public-bugbounty-programs/main/hackerone_data.json"
    data = fetch_json(url)
    domains = [p["domains"][0] for p in data.get("programs", []) if p.get("domains")]
    print(f"🔹 HackerOne → {len(domains)} targets")
    return domains[:limit]

# ---------------------- Bugcrowd ----------------------

def fetch_bugcrowd_targets(limit=200):
    print("🧠 Fetching Bugcrowd programs...")
    url = "https://raw.githubusercontent.com/projectdiscovery/public-bugbounty-programs/main/bugcrowd_data.json"
    data = fetch_json(url)
    domains = [p["domains"][0] for p in data.get("programs", []) if p.get("domains")]
    print(f"🔹 Bugcrowd → {len(domains)} targets")
    return domains[:limit]

# ---------------------- Intigriti ----------------------

def fetch_intigriti_targets(limit=200):
    print("🧠 Fetching Intigriti programs...")
    url = "https://raw.githubusercontent.com/projectdiscovery/public-bugbounty-programs/main/intigriti_data.json"
    data = fetch_json(url)
    domains = [p["domains"][0] for p in data.get("programs", []) if p.get("domains")]
    print(f"🔹 Intigriti → {len(domains)} targets")
    return domains[:limit]

# ---------------------- YesWeHack ----------------------

def fetch_yeswehack_targets(limit=200):
    print("🧠 Fetching YesWeHack programs...")
    url = "https://raw.githubusercontent.com/projectdiscovery/public-bugbounty-programs/main/yeswehack_data.json"
    data = fetch_json(url)
    domains = [p["domains"][0] for p in data.get("programs", []) if p.get("domains")]
    print(f"🔹 YesWeHack → {len(domains)} targets")
    return domains[:limit]

# ---------------------- Immunefi (Web3/Crypto) ----------------------

def fetch_immunefi_targets(limit=200):
    print("🧠 Fetching Immunefi programs...")
    url = "https://raw.githubusercontent.com/projectdiscovery/public-bugbounty-programs/main/immunefi_data.json"
    data = fetch_json(url)
    domains = [p["domains"][0] for p in data.get("programs", []) if p.get("domains")]
    print(f"🔹 Immunefi → {len(domains)} targets")
    return domains[:limit]

# ---------------------- Main Orchestrator ----------------------

def generate_intelligence_feed(limit=1000):
    print("🚀 [Digital Sentinel Intel Feed Generator v∞] Starting up...")
    all_targets = []

    all_targets += fetch_hackerone_targets(limit=limit//5)
    all_targets += fetch_bugcrowd_targets(limit=limit//5)
    all_targets += fetch_intigriti_targets(limit=limit//5)
    all_targets += fetch_yeswehack_targets(limit=limit//5)
    all_targets += fetch_immunefi_targets(limit=limit//5)

    print("🧩 Deduplicating targets...")
    unique_targets = sorted(set(all_targets))[:limit]
    write_targets(unique_targets)

    print(f"✅ Intelligence Feed Generated: {len(unique_targets)} total targets.")
    print(f"🕒 Timestamp: {datetime.utcnow().isoformat()}Z")
    print("🌐 Legal and safe for Bug Bounty scanning only.")
    return unique_targets

# ---------------------- CLI Entrypoint ----------------------

if __name__ == "__main__":
    generate_intelligence_feed(limit=MAX_TARGETS)
