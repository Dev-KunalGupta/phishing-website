import pandas as pd
from engine.feature_extractor import extract_url_features
import random

PHISHING_FILE = "models/online-valid.csv"   # change if needed
LEGIT_FILE = "models/top-1m.csv"
OUTPUT_FILE = "models/training_data.csv"

def load_phishing_urls():
    print("Loading phishing URLs...")
    df = pd.read_csv(PHISHING_FILE)
    urls = df["url"].dropna().unique()
    return urls[:2500]   # Increased size

def generate_legit_variations(domain):
    variations = []

    # Base
    variations.append(f"https://{domain}")

    # Common legit paths
    variations.append(f"https://{domain}/login")
    variations.append(f"https://{domain}/account")
    variations.append(f"https://{domain}/home")

    # Query parameter example
    variations.append(f"https://{domain}/profile?id={random.randint(1,9999)}")

    # Subdomain example
    variations.append(f"https://mail.{domain}")

    return variations

def load_legit_urls():
    print("Loading legitimate domains...")
    df = pd.read_csv(LEGIT_FILE, header=None)

    domains = df[1].dropna().unique()[:500]  # 500 base domains

    legit_urls = []

    for domain in domains:
        variations = generate_legit_variations(domain)
        legit_urls.extend(variations)

    return legit_urls[:2500]  # Ensure balance

def build_dataset():

    phishing_urls = load_phishing_urls()
    legit_urls = load_legit_urls()

    data = []

    print("Extracting phishing features...")
    for url in phishing_urls:
        try:
            features = extract_url_features(url)
            features["label"] = 1
            data.append(features)
        except:
            continue

    print("Extracting legitimate features...")
    for url in legit_urls:
        try:
            features = extract_url_features(url)
            features["label"] = 0
            data.append(features)
        except:
            continue

    df = pd.DataFrame(data)
    df.to_csv(OUTPUT_FILE, index=False)

    print("Dataset saved to:", OUTPUT_FILE)
    print("Total samples:", len(df))
    print("Phishing samples:", len(phishing_urls))
    print("Legitimate samples:", len(legit_urls))

if __name__ == "__main__":
    build_dataset()
