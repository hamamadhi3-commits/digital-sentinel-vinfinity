#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
crawling_engine.py
------------------
Responsible for crawling discovered live targets to extract:
 - JavaScript files
 - internal endpoints
 - technology fingerprints
 - metadata for further reconnaissance

This is a lightweight crawler optimized for Digital Sentinel vInfinity.
It works without external APIs, purely local scanning and pattern extraction.
"""

import os
import requests
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup

# ✅ Optional: safe headers for crawling
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (compatible; DigitalSentinelBot/12.0; "
        "+https://github.com/hamamadhii3/digital-sentinel-vinfinity)"
    )
}

CRAWL_RESULTS_DIR = os.path.join("data", "results", "crawling_reports")


def run_crawling(targets_file: str = "data/targets.txt", max_depth: int = 1):
    """
    Crawl live targets and collect internal links, JS files, and endpoints.
    Saves results into data/results/crawling_reports/{domain}.txt
    """
    os.makedirs(CRAWL_RESULTS_DIR, exist_ok=True)

    try:
        with open(targets_file, "r", encoding="utf-8") as f:
            targets = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"⚠️ [Crawler] Target file not found: {targets_file}")
        return []

    print(f"🕷️ [Crawler] Starting crawl for {len(targets)} targets...")

    crawled_results = []

    for target in targets:
        url = f"https://{target}" if not target.startswith("http") else target
        domain = urlparse(url).netloc
        output_path = os.path.join(CRAWL_RESULTS_DIR, f"{domain}.txt")

        try:
            print(f"🌐 Crawling {url} ...")
            response = requests.get(url, headers=HEADERS, timeout=10)
            soup = BeautifulSoup(response.text, "html.parser")

            found_links = set()
            js_files = set()

            for link in soup.find_all("a", href=True):
                href = urljoin(url, link["href"])
                if domain in href:
                    found_links.add(href)

            for script in soup.find_all("script", src=True):
                src = urljoin(url, script["src"])
                js_files.add(src)

            # Save results
            with open(output_path, "w", encoding="utf-8") as out:
                out.write(f"# Crawling report for {domain}\n")
                out.write(f"# Total internal links: {len(found_links)}\n")
                out.write(f"# Total JS files: {len(js_files)}\n\n")

                out.write("[Internal Links]\n")
                for l in found_links:
                    out.write(l + "\n")

                out.write("\n[JavaScript Files]\n")
                for j in js_files:
                    out.write(j + "\n")

            crawled_results.append({
                "domain": domain,
                "links": len(found_links),
                "scripts": len(js_files)
            })
            print(f"✅ [Crawler] {domain} → {len(found_links)} links, {len(js_files)} JS files")

        except Exception as e:
            print(f"⚠️ [Crawler] Error crawling {target}: {e}")

    print("🧩 Crawling complete.")
    return crawled_results


if __name__ == "__main__":
    run_crawling()
