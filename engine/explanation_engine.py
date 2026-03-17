def generate_explanation(features, rule_score, final_risk, classification):

    reasons = []

    # Structural Reasons
    if features["has_ip"]:
        reasons.append("The URL uses an IP address instead of a domain name.")

    if features["suspicious_tld"]:
        reasons.append("The domain uses a high-risk top-level domain.")

    if features["suspicious_keyword"]:
        reasons.append("The URL contains authentication-related keywords.")

    if not features["has_https"]:
        reasons.append("The website does not use HTTPS encryption.")

    if features["domain_entropy"] > 3.5:
        reasons.append("The domain appears randomly generated (high entropy).")

    if features["num_digits"] > 5:
        reasons.append("The URL contains an excessive number of numeric digits.")

    if features["num_hyphens"] > 2:
        reasons.append("The domain contains multiple hyphens, which is suspicious.")

    if features["num_dots"] > 3:
        reasons.append("The URL has multiple subdomains which may indicate spoofing.")

    # Default message if no strong reason
    if not reasons:
        reasons.append("No strong phishing indicators were detected.")

    # Recommendation logic
    if classification == "Phishing":
        recommendation = "Avoid visiting this website and do not enter any personal information."
    elif classification == "Suspicious":
        recommendation = "Proceed with caution. Verify the legitimacy of the website before interacting."
    else:
        recommendation = "The website appears safe, but always remain cautious online."

    return {
        "reasons": reasons,
        "recommendation": recommendation
    }
