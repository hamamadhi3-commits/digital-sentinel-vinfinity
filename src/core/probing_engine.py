"""
Digital Sentinel - Crawling Engine
==================================
This module crawls alive targets discovered in the probing phase.
It collects links and JavaScript endpoints for deeper analysis.
"""

import os
import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed

# Paths
SRC_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
DATA_PATH = os.path.join(SRC_PATH, "data")
INPUT_FILE = os.path.join(DATA_PATH, "cache", "validated", "alive_hosts.txt")
OUTPUT_FILE = os.path.join(DATA_PATH, "cache", "crawled", "urls.txt")


def crawl_target(target: str, depth: int = 1):
    """Fetch and parse links from the target's homepage."""
    urls = set()
    base_url = f"https://{target}"
    try:
        r = requests.get(base_url, timeout=8, verify=False)
        soup = BeautifulSoup(r.text, "html.parser")
        for link in soup.find_all("a", href=True):
            href = link["href"]
            if href.startswith("http"):
                urls.add(href)
            elif href.startswith("/"):
                urls.add(base_url + href)
    except Exception as e:
        print(f"⚠️ Crawl failed for {target}: {e}")
    return urls


def run_crawling():
    """Main crawling entry point."""
    print("🕸️ [Phase 3: Crawling Engine Started]")

    if not os.path.exists(INPUT_FILE):
        print(f"⚠️ No alive hosts found at {INPUT_FILE}")
        return

    with open(INPUT_FILE, "r") as f:
        targets = [line.strip() for line in f if line.strip()]

    all_urls = set()
    with ThreadPoolExecutor(max_workers=20) as executor:
        futures = {executor.submit(crawl_target, t): t for t in targets}
        for future in as_completed(futures):
            target = futures[future]
            try:
                urls = future.result()
                all_urls.update(urls)
                print(f"✅ Crawled {len(urls)} URLs from {target}")
            except Exception as e:
                print(f"⚠️ Error crawling {target}: {e}")

    # Save results
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, "w") as f:
        for url in sorted(all_urls):
            f.write(url + "\n")

    print(f"\n💾 Saved {len(all_urls)} URLs to {OUTPUT_FILE}")
    print("🔚 [Phase 3 Completed - Crawling Engine]\n")
