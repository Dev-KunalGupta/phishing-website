def calculate_rule_risk(features):

    risk_score = 0
    high_severity_count = 0

    # HIGH SEVERITY RULES
    if features["has_ip"]:
        risk_score += 25
        high_severity_count += 1

    if features["domain_entropy"] > 3.5:
        risk_score += 20
        high_severity_count += 1

    # MEDIUM SEVERITY RULES
    if features["suspicious_tld"]:
        risk_score += 15

    if features["suspicious_keyword"]:
        risk_score += 15

    if not features["has_https"]:
        risk_score += 10

    # LOW SEVERITY RULES
    if features["num_digits"] > 5:
        risk_score += 8

    if features["num_hyphens"] > 2:
        risk_score += 8

    if features["num_dots"] > 3:
        risk_score += 8

    # Escalation Logic
    if high_severity_count >= 2:
        risk_score *= 1.2

    # Critical Override
    if features["has_ip"] and features["suspicious_keyword"]:
        risk_score = max(risk_score, 75)

    return min(int(risk_score), 100)
