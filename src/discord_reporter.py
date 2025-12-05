#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Digital Sentinel Discord Reporter vInfinity
Sends final AI-analyzed vulnerability reports to Discord channels.
"""

import os
import json
import requests

DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL", "").strip()

def send_discord_report(report_path, summary=None):
    """Send a report file and summary to a configured Discord webhook."""
    if not DISCORD_WEBHOOK_URL:
        print("⚠️ Discord webhook not configured (missing DISCORD_WEBHOOK_URL). Skipping send.")
        return

    try:
        with open(report_path, "r", encoding="utf-8") as f:
            report_data = f.read()
    except Exception as e:
        print(f"❌ Failed to open report file: {e}")
        return

    payload = {
        "username": "🛡️ Digital Sentinel",
        "content": f"📡 **New Quantum Scan Report Uploaded**\nSummary:\n{summary or 'No summary provided.'}",
        "embeds": [
            {
                "title": "Scan Report",
                "description": f"```json\n{report_data[:1500]}\n```",
                "color": 3447003
            }
        ]
    }

    try:
        response = requests.post(DISCORD_WEBHOOK_URL, json=payload)
        if response.status_code == 204:
            print("✅ Discord report sent successfully.")
        else:
            print(f"⚠️ Discord send failed — HTTP {response.status_code}")
    except Exception as e:
        print(f"💥 Discord reporting error: {e}")
