#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Digital Sentinel Enumeration Engine vInfinity
Responsible for discovering active subdomains and preparing the intelligence layer for probing.
"""

import os
import subprocess
import time
from datetime import datetime


# ===================== ⚙️ Configuration =====================
DATA_DIR = "data"
TARGET_FILE = os.path.join(DATA_DIR, "targets.txt")
RESULTS_DIR = os.path.join(DATA_DIR, "results")
ENUM_LOG = os.path.join(RESULTS_DIR, "enumeration.log")

os.makedirs(RESULTS_DIR, exist_ok=True)
# ============================================================


def log_event(message: str):
    """Append log message to enumeration.log"""
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    with open(ENUM_LOG, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {message}\n")
    print(message)


def read_targets():
    """Load target domains from targets.txt"""
    if not os.path.exists(TARGET_FILE):
        log_event("⚠️ No targets.txt found! Please generate it first via intel_feed_generator.")
        return []

    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        targets = [line.strip() for line in f if line.strip()]
    log_event(f"📥 Loaded {len(targets)} targets from {TARGET_FILE}")
    return targets


def enumerate_subdomains(domain: str):
    """
    Perform subdomain enumeration for a given domain.
    You can later replace this mock implementation with real tools like subfinder or amass.
    """
    log_event(f"🌐 Enumerating subdomains for: {domain}")
    # Example simulation
    subdomains = [
        f"api.{domain}",
        f"dev.{domain}",
        f"staging.{domain}",
        f"mail.{domain}",
        f"www.{domain}"
    ]
    time.sleep(1)
    log_event(f"✅ Enumeration for {domain} finished — {len(subdomains)} subdomains found.")
    return subdomains


def run_enumeration(targets_file: str = TARGET_FILE):
    """
    Main entrypoint for enumeration — called by main_controller_v11_4_quantum.py.
    Reads targets from file, enumerates subdomains, and stores results.
    """
    log_event("🚀 Enumeration engine started.")
    targets = read_targets()
    all_subdomains = []

    for target in targets:
        try:
            found = enumerate_subdomains(target)
            all_subdomains.extend(found)
        except Exception as e:
            log_event(f"❌ Error enumerating {target}: {e}")

    # Save results
    out_file = os.path.join(RESULTS_DIR, "subdomains.txt")
    with open(out_file, "w", encoding="utf-8") as f:
        f.write("\n".join(all_subdomains))

    log_event(f"💾 Saved {len(all_subdomains)} total subdomains → {out_file}")
    log_event("✅ Enumeration phase complete.\n")
    return all_subdomains


# Standalone execution (for testing)
if __name__ == "__main__":
    print("🔍 Running Enumeration Engine standalone mode...")
    result = run_enumeration()
    print(f"✅ Finished with {len(result)} subdomains total.")
