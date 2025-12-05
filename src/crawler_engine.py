#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
crawling_engine.py
------------------
Crawls discovered targets to collect internal links and JavaScript files.
Stores reports in data/results/crawling_reports/{domain}.txt
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
    """Crawl live targets and extract internal links & JS files."""
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
            r = requests.get(url, headers=HEADERS, timeout=8)
            soup = BeautifulSoup(r.text, "html.parser")

            links = {urljoin(url, a["href"]) for a in soup.find_all("a", href=True) if domain in urljoin(url, a["href"])}
            js_files = {urljoin(url, s["src"]) for s in soup.find_all("script", src=True)}

            with open(output_path, "w", encoding="utf-8") as out:
                out.write(f"# Report for {domain}\n\n[Links]\n")
                for l in links: out.write(l + "\n")
                out.write("\n[JS Files]\n")
                for j in js_files: out.write(j + "\n")

            print(f"✅ [Crawler] {domain} → {len(links)} links, {len(js_files)} JS files")
            crawled_results.append({"domain": domain, "links": len(links), "scripts": len(js_files)})

        except Exception as e:
            print(f"⚠️ [Crawler] Error crawling {target}: {e}")

    print("🧩 Crawling complete.")
    return crawled_results


if __name__ == "__main__":
    run_crawling()
