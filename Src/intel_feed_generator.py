import random, os

def generate_targets():
    os.makedirs("data", exist_ok=True)
    targets = [
        "tesla.com", "apple.com", "microsoft.com", "google.com",
        "bugcrowd.com", "hackerone.com", "intel.com", "amazon.com",
        "adobe.com", "paypal.com", "spotify.com", "dropbox.com"
    ]
    with open("data/targets.txt", "w") as f:
        for t in random.sample(targets, len(targets)):
            f.write(t + "\n")
    print("🧩 Intelligence feed updated → targets.txt")

if __name__ == "__main__":
    generate_targets()
