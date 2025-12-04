# ============================================
#  DIGITAL SENTINEL QUANTUM IMMORTAL LOOP v∞
# ============================================

import time, subprocess, random
from datetime import datetime

def evolve_cycle():
    print(f"\n🚀 [Quantum-∞] Cycle start @ {datetime.now()}")
    subprocess.run(["python3", "src/intel_feed_generator.py"])
    subprocess.run(["python3", "src/main_controller_v11_4_quantum.py"])
    print("✅ [Quantum-∞] Cycle complete\n")

if __name__ == "__main__":
    print("♾️ Digital Sentinel Quantum Immortal Loop — ACTIVE")
    cycle_count = 0
    while True:
        evolve_cycle()
        cycle_count += 1
        wait = random.randint(10, 60)
        print(f"⏱ Waiting {wait}s before next evolution cycle ({cycle_count} total)\n")
        time.sleep(wait)
