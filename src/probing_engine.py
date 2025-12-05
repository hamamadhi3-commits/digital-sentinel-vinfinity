#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Digital Sentinel Probing Engine vInfinity
Checks which enumerated subdomains are alive using simulated HTTP probing.
"""

import os
import time
from datetime import datetime

RESULTS_DIR = "data/results"
PROBE_LOG = os.path.join(RESULTS_DIR, "probing.log")
os.makedirs(RESULTS_DIR, exist_ok=True)


def log_event(message: str):
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    with open(PROBE_LOG, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {message}\n")
    print(message)


def run_probing(subdomains: list):
    """Simulated HTTP probing — mark 30% as alive (for now)."""
    log_event("🔎 Probing live hosts...")

    alive = []
    for idx, host in enumerate(subdomains):
        if idx % 3 == 0:  # simulate success rate
            alive.append(host)
        time.sleep(0.001)

    log_event(f"✅ Probing complete — {len(alive)} live domains active.")
    return alive


if __name__ == "__main__":
    sample = ["api.example.com", "dev.example.com", "mail.example.com"]
    run_probing(sample)
