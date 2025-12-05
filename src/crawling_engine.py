#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
crawling_engine.py
------------------
Stable version with:
  • SSL verification bypass option
  • DNS resolution resilience
  • Timeout handling
  • Smart logging for unreachable targets
"""

import os
import requests
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup

# 🧠 Base headers for all HTTP requests
HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; DigitalSentinelBot/15.0; +https://github.com/hamamadhii3)"
}

CRAWL_RESULTS_DIR = os.path.join("data", "results", "crawling_reports")
TIMEOUT = 10  # seconds
VERIFY_SSL = False  # disable SSL verification errors safely


def run_crawling(targets_input):
    """
    Crawl list of targets or path to file.
    Returns list of dict results with domain/link/script stats.
    """
    os.makedirs(CRAWL_RESULTS_DIR, exist_ok=True)

    # Detect type of input
    if isinstance(targets_input, list):
        targets = targets_input
    elif isinstance(targets_input, str) and os.path.exists(targets_input):
        with open(targets_input, "r", encoding="utf-8") as f:
            targets = [line.strip() for line in f if line.strip()]
    else:
        print(f"⚠️ [Crawler] Invalid input provided: {type(targets_input)}")
        return []

    print(f"🕷️ [Crawler] Starting crawl for {len(targets)} targets...")
    results = []
    unreachable = []

    for t in targets:
        url = f"https://{t}" if not t.startswith("http") else t
        domain = urlparse(url).netloc or t
        out_file = os.path.join(CRAWL_RESULTS_DIR, f"{domain}.txt")

        try:
            print(f"🌐 Crawling {url} ...")
            r = requests.get(url, headers=HEADERS, timeout=TIMEOUT, verify=VERIFY_SSL)
            r.raise_for_status()
            soup = BeautifulSoup(r.text, "html.parser")

            links = set()
            js_files = set()

            for a in soup.find_all("a", href=True):
                href = urljoin(url, a["href"])
                if domain in href:
                    links.add(href)

            for s in soup.find_all("script", src=True):
                js_files.add(urljoin(url, s["src"]))

            with open(out_file, "w", encoding="utf-8") as f:
                f.write(f"# Report for {domain}\n")
                f.write(f"# Links: {len(links)} | JS Files: {len(js_files)}\n\n")
                f.write("[Internal Links]\n")
                for l in links:
                    f.write(l + "\n")
                f.write("\n[JavaScript Files]\n")
                for j in js_files:
                    f.write(j + "\n")

            print(f"✅ [Crawler] {domain} → {len(links)} links, {len(js_files)} JS files")
            results.append({"domain": domain, "links": len(links), "scripts": len(js_files)})

        except requests.exceptions.SSLError:
            print(f"⚠️ [Crawler] SSL verification failed for {url} (ignored)")
            unreachable.append(url)
        except requests.exceptions.ConnectionError as ce:
            print(f"⚠️ [Crawler] DNS/Connection error: {url} → {ce}")
            unreachable.append(url)
        except requests.exceptions.Timeout:
            print(f"⚠️ [Crawler] Timeout: {url} > {TIMEOUT}s")
            unreachable.append(url)
        except Exception as e:
            print(f"⚠️ [Crawler] Unknown error on {url}: {e}")
            unreachable.append(url)

    # Save summary
    summary_file = os.path.join(CRAWL_RESULTS_DIR, "summary.txt")
    with open(summary_file, "w", encoding="utf-8") as s:
        s.write("# Digital Sentinel Crawl Summary\n")
        s.write(f"Total targets: {len(targets)}\n")
        s.write(f"Successful: {len(results)}\n")
        s.write(f"Failed: {len(unreachable)}\n\n")
        if unreachable:
            s.write("[Unreachable Targets]\n")
            for u in unreachable:
                s.write(u + "\n")

    print("🧩 Crawling complete.")
    print(f"✅ Success: {len(results)} | ⚠️ Failed: {len(unreachable)}")
    return results


if __name__ == "__main__":
    run_crawling("data/targets.txt")
