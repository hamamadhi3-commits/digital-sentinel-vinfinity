#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Digital Sentinel Core Package Initializer
----------------------------------------
This file initializes the core package of the Digital Sentinel Quantum System.
It links internal modules together such as:
 - intel_feed_generator: Handles target list updates from authorized bug bounty sources
 - discord_reporter: Manages sending results and alerts to Discord
 - shared logging functions (optional future expansion)
"""

# ✅ Import the proper reporter function (not the old class)
from src.discord_reporter import send_discord_report

# ✅ Import the intelligence feed generator
from src.core.intel_feed_generator import generate_intel_feed

__all__ = [
    "send_discord_report",
    "generate_intel_feed"
]
