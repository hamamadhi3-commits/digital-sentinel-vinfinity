#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
intel_feed_generator.py
-----------------------
Core intelligence feed generator for Digital Sentinel vInfinity.
This module automatically builds and refreshes the `data/targets.txt` list
using known bug bounty program domains from trusted platforms (Bugcrowd, HackerOne, Intigriti, YesWeHack, etc.).
It does NOT use APIs — only static curated data sources.

Author: QuantumForge AI Division
"""

import os
import random
import datetime

# ✅ Local paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
TARGETS_PATH = os.path.join(BASE_DIR, "data", "targets.txt")

# ✅ Default Bug Bounty Platforms
BUG_BOUNTY_SOURCES = {
    "bugcrowd": [
        "tesla.com", "paypal.com", "shopify.com", "atlassian.com", "okta.com",
        "sendgrid.com", "bitdefender.com", "jetbrains.com", "sony.com", "westernunion.com"
    ],
    "hackerone": [
        "hackerone.com", "twitter.com", "github.com", "gitlab.com", "dropbox.com",
        "cloudflare.com", "uber.com", "yelp.com", "linkedin.com", "pinterest.com"
    ],
    "intigriti": [
        "booking.com", "rakuten.com", "bosch.com", "acer.com", "tomtom.com",
        "belgium.be", "zalando.com", "vodafone.de", "kaspersky.com", "axa.com"
    ],
    "yeswehack": [
        "orange.fr", "airbus.com", "soprahr.com", "edf.fr", "renault.com",
        "thalesgroup.com", "veolia.com", "capgemini.com", "suez.com", "axa.fr"
    ]
}

def generate_intel_feed():
    """
    Generates and refreshes the target intelligence feed.
    Creates data/targets.txt with a randomized and deduplicated list of target domains.
    """
    try:
        print("🧠 [IntelFeed] Generating updated target list...")
        
        # Combine all platform domains
        combined_targets = []
        for platform, domains in BUG_BOUNTY_SOURCES.items():
            for domain in domains:
                combined_targets.append(domain)
        
        # Deduplicate + shuffle
        unique_targets = list(set(combined_targets))
        random.shuffle(unique_targets)

        # Write to file
        os.makedirs(os.path.dirname(TARGETS_PATH), exist_ok=True)
        with open(TARGETS_PATH, "w", encoding="utf-8") as f:
            for target in unique_targets:
                f.write(f"{target}\n")

        print(f"✅ Intelligence feed updated → {TARGETS_PATH}")
        print(f"📦 Total bug bounty targets: {len(unique_targets)}")

        return unique_targets

    except Exception as e:
        print(f"⚠️ [IntelFeed] Failed to update targets.txt: {e}")
        return []


if __name__ == "__main__":
    print("🚀 Running intel_feed_generator standalone mode...")
    generate_intel_feed()
    print("🧩 Feed generation completed successfully.")
