#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
crawling_engine.py
------------------
Core web crawler for Digital Sentinel.
Crawls each target from targets.txt and extracts internal links + JS files.
"""

import os
import requests
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; DigitalSentinelBot/12.0; +https://github.com/hamamadhii3)"
}

CRAWL_RESULTS_DIR = os.path.join("data", "results", "crawling_reports")

def run_crawling(targets_file: str = "data/targets.txt"):
    os.makedirs(CRAWL_RESULTS_DIR, exist_ok=True)
    if not os.path.exists(targets_file):
        print(f"⚠️ [Crawler] Missing targets file: {targets_file}")
        return []

    with open(targets_file, "r", encoding="utf-8") as f:
        targets = [line.strip() for line in f if line.strip()]

    print(f"🕷️ [Crawler] Starting crawl for {len(targets)} targets...")
    results = []

    for t in targets:
        url = f"https://{t}" if not t.startswith("http") else t
        domain = urlparse(url).netloc
        out_file = os.path.join(CRAWL_RESULTS_DIR, f"{domain}.txt")

        try:
            print(f"🌐 Crawling {url} ...")
            r = requests.get(url, headers=HEADERS, timeout=8)
            soup = BeautifulSoup(r.text, "html.parser")

            links = set()
            js_files = set()

            for a in soup.find_all("a", href=True):
                href = urljoin(url, a["href"])
                if domain in href:
                    links.add(href)

            for s in soup.find_all("script", src=True):
                src = urljoin(url, s["src"])
                js_files.add(src)

            with open(out_file, "w", encoding="utf-8") as f:
                f.write(f"# Report for {domain}\n")
                f.write(f"# Links: {len(links)} | JS Files: {len(js_files)}\n\n")
                f.write("[Internal Links]\n")
                for l in links:
                    f.write(l + "\n")
                f.write("\n[JavaScript Files]\n")
                for j in js_files:
                    f.write(j + "\n")

            print(f"✅ [Crawler] {domain} → {len(links)} links, {len(js_files)} JS")
            results.append({"domain": domain, "links": len(links), "scripts": len(js_files)})

        except Exception as e:
            print(f"⚠️ [Crawler] Error on {url}: {e}")

    print("🧩 Crawling complete.")
    return results


if __name__ == "__main__":
    run_crawling()
