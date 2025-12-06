"""
Digital Sentinel - Crawling Engine
==================================
Simulates crawling step by saving results to data/cache/crawled/.
"""

import os
import time

def run_crawling():
    """Main crawling phase — simulates basic site crawling."""
    print("🚀 [Phase 3: Crawling Engine Started]")

    output_dir = os.path.join("data", "cache", "crawled")
    os.makedirs(output_dir, exist_ok=True)

    output_file = os.path.join(output_dir, "crawl_results.txt")

    # Simulate crawling
    print("🔍 Crawling in progress...")
    time.sleep(2)  # simulate delay
    with open(output_file, "w") as f:
        f.write("https://example.com/page1\n")
        f.write("https://example.com/page2\n")
        f.write("https://example.com/page3\n")

    print(f"✅ Crawling results saved to {output_file}")
    print("🔚 [Phase 3: Crawling Completed]")


if __name__ == "__main__":
    run_crawling()
