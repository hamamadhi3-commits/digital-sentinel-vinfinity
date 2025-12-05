#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
intel_feed_generator.py
-----------------------
Generates or refreshes the Bug Bounty intelligence feed.

This module safely updates the master `data/targets.txt` file
with authorized bug bounty program domains (e.g. Bugcrowd, HackerOne, Intigriti, etc.)
and supports external trigger calls from Quantum Controller.
"""

import os
import json
from datetime import datetime

# Default intelligence directory
DATA_DIR = "data"
TARGET_FILE = os.path.join(DATA_DIR, "targets.txt")
EXPORT_DIR = os.path.join(DATA_DIR, "results", "bugcrowd_exports")

# Example static authorized targets (you can expand or update dynamically)
DEFAULT_TARGETS = [
    "bugcrowd.com",
    "hackerone.com",
    "intigriti.com",
    "yeswehack.com",
    "tesla.com",
    "paypal.com",
    "spotify.com",
    "adobe.com",
    "google.com",
    "apple.com",
    "amazon.com",
    "dropbox.com",
    "intel.com",
    "microsoft.com",
]


def generate_intel_feed(*args, **kwargs):
    """
    Refresh the main intelligence feed.

    - Creates data/targets.txt if missing.
    - Updates it with all known safe-to-scan Bug Bounty programs.
    - Logs an intelligence summary to JSON format.
    - Can be called both manually or automatically (no crash if args passed).
    """

    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(EXPORT_DIR, exist_ok=True)

    # If custom targets are passed in kwargs, merge them
    custom_targets = kwargs.get("custom_targets", [])
    all_targets = sorted(set(DEFAULT_TARGETS + custom_targets))

    try:
        with open(TARGET_FILE, "w", encoding="utf-8") as f:
            for t in all_targets:
                f.write(t.strip() + "\n")

        # Log a lightweight feed summary for reference
        feed_info = {
            "timestamp": datetime.utcnow().isoformat(),
            "total_targets": len(all_targets),
            "source": "Digital Sentinel v∞ Quantum Intel Feed",
            "targets": all_targets,
        }

        json_path = os.path.join(EXPORT_DIR, "intel_feed_summary.json")
        with open(json_path, "w", encoding="utf-8") as jf:
            json.dump(feed_info, jf, indent=2)

        print(f"🧩 Intelligence feed updated → {TARGET_FILE}")
        print(f"✅ {len(all_targets)} authorized targets saved successfully.")
        return feed_info

    except Exception as e:
        print(f"⚠️ [Intel] Failed to generate feed: {e}")
        return {"error": str(e)}


if __name__ == "__main__":
    # Run standalone mode for testing
    print("⚙️ Running standalone Intel Feed Generator...")
    info = generate_intel_feed()
    print(json.dumps(info, indent=2))
