import concurrent.futures
import subprocess
import os
import time

TARGETS_FILE = "data/targets.txt"
MAX_THREADS = 100  # 🔥 Parallel threads limit (scan 100 targets at once)
OUTPUT_DIR = "data/results/"

os.makedirs(OUTPUT_DIR, exist_ok=True)

def scan_target(target):
    """Run reconnaissance and vulnerability scan for one target."""
    try:
        start_time = time.strftime("%H:%M:%S")
        print(f"[{start_time}] 🛰 Scanning: {target}")
        cmd = [
            "bash", "-c",
            f"subfinder -d {target} -silent | httpx -silent -mc 200,403,401 -threads 50 | tee {OUTPUT_DIR}{target}.txt"
        ]
        subprocess.run(cmd, check=True)
        print(f"✅ Finished: {target}")
    except Exception as e:
        print(f"❌ Error scanning {target}: {e}")

def main():
    with open(TARGETS_FILE, "r") as f:
        targets = [line.strip() for line in f if line.strip()]

    print(f"🚀 Starting parallel scan for {len(targets)} targets...")

    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        futures = {executor.submit(scan_target, target): target for target in targets}
        for future in concurrent.futures.as_completed(futures):
            target = futures[future]
            try:
                future.result()
            except Exception as exc:
                print(f"⚠️ Target {target} generated an exception: {exc}")

    print("🎯 All scans completed successfully.")

if __name__ == "__main__":
    main()
