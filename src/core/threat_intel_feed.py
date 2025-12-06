import json, requests, datetime, os

DATA_DIR = "data/feeds"
os.makedirs(DATA_DIR, exist_ok=True)

def fetch_alienvault_otx():
    url = "https://otx.alienvault.com/api/v1/pulses/subscribed"
    try:
        r = requests.get(url, timeout=15)
        data = r.json()
        results = []
        for pulse in data.get("results", []):
            for ioc in pulse.get("indicators", []):
                results.append({
                    "type": ioc.get("type"),
                    "indicator": ioc.get("indicator"),
                    "title": pulse.get("name"),
                    "date": pulse.get("modified")
                })
        with open(f"{DATA_DIR}/ioc_feed.json", "w") as f:
            json.dump(results, f, indent=2)
        return len(results)
    except Exception as e:
        print(f"[!] AlienVault fetch error: {e}")
        return 0

def fetch_cisa_kev():
    url = "https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json"
    try:
        r = requests.get(url, timeout=15)
        kev = r.json()
        vulns = kev.get("vulnerabilities", [])
        with open(f"{DATA_DIR}/cve_feed.json", "w") as f:
            json.dump(vulns, f, indent=2)
        return len(vulns)
    except Exception as e:
        print(f"[!] CISA fetch error: {e}")
        return 0

def fetch_abuseipdb():
    url = "https://api.abuseipdb.com/api/v2/blacklist"
    headers = {"Key": os.getenv("ABUSEIPDB_API_KEY", ""), "Accept": "application/json"}
    try:
        r = requests.get(url, headers=headers, timeout=15)
        ip_data = r.json()
        with open(f"{DATA_DIR}/ip_feed.json", "w") as f:
            json.dump(ip_data, f, indent=2)
        return len(ip_data.get("data", []))
    except Exception as e:
        print(f"[!] AbuseIPDB fetch error: {e}")
        return 0

def run_threat_feed():
    print("🛰️ [Phase 10: Threat Intelligence Feed Started]")
    total = 0
    total += fetch_alienvault_otx()
    total += fetch_cisa_kev()
    total += fetch_abuseipdb()
    print(f"📡 Total feeds collected: {total}")
    print("✅ [Phase 10: Threat Intelligence Feed Completed]")
    return total
