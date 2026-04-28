import re
import math
from urllib.parse import urlparse
import pandas as pd
import tldextract

# Load top domains once
try:
    top_domains_df = pd.read_csv("models/top-1m.csv", header=None)
    TOP_DOMAINS = set(top_domains_df[1].head(10000))
except:
    TOP_DOMAINS = set()


def calculate_entropy(domain):
    if not domain:
        return 0
    prob = [float(domain.count(c)) / len(domain) for c in set(domain)]
    entropy = -sum([p * math.log2(p) for p in prob])
    return entropy


def extract_url_features(url):

    parsed = urlparse(url)

    # Domain extraction
    ext = tldextract.extract(url)
    domain = (ext.subdomain + "." + ext.domain + "." + ext.suffix).strip(".")
    root_domain = ext.domain + "." + ext.suffix

    # Handle empty cases
    if root_domain == ".":
        root_domain = domain

    is_popular = 1 if root_domain in TOP_DOMAINS else 0

    features = {}

    # Basic length features
    features["url_length"] = len(url)
    features["domain_length"] = len(domain)
    features["path_length"] = len(parsed.path)

    # Structural counts
    features["num_dots"] = url.count(".")
    features["num_hyphens"] = url.count("-")
    features["num_digits"] = sum(c.isdigit() for c in url)
    features["num_special_chars"] = len(re.findall(r"[!@#$%^&*(),?\":{}|<>]", url))
    features["num_subdirs"] = url.count("/")
    features["num_query_params"] = len(parsed.query.split("&")) if parsed.query else 0

    # Boolean indicators
    features["has_ip"] = 1 if re.match(r"\d+\.\d+\.\d+\.\d+", domain) else 0
    features["has_at"] = 1 if "@" in url else 0
    features["has_https"] = 1 if parsed.scheme == "https" else 0
    features["has_port"] = 1 if ":" in domain else 0

    # Suspicious keywords
    suspicious_keywords = [
        "login", "verify", "account", "secure", "update",
        "bank", "paypal", "signin", "confirm", "password"
    ]
    features["suspicious_keyword"] = 1 if any(word in url.lower() for word in suspicious_keywords) else 0

    # Suspicious TLDs
    suspicious_tlds = [".xyz", ".tk", ".ml", ".ga", ".cf"]
    features["suspicious_tld"] = 1 if any(root_domain.endswith(tld) for tld in suspicious_tlds) else 0

    # Entropy (only for root domain, not full)
    features["domain_entropy"] = calculate_entropy(root_domain)

    # POPULAR DOMAIN FEATURE
    features["is_popular_domain"] = is_popular

    return features