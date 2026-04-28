def calculate_rule_risk(features):

    risk_score = 0
    high_severity_count = 0

    # HIGH SEVERITY
    if features["has_ip"]:
        risk_score += 30
        high_severity_count += 1

    # Reduce entropy importance
    if features["domain_entropy"] > 4.0:  
        risk_score += 10  

    # MEDIUM
    if features["suspicious_tld"]:
        risk_score += 15

    if features["suspicious_keyword"]:
        risk_score += 12   # reduced

    if not features["has_https"]:
        risk_score += 5  

    # LOW
    if features["num_digits"] > 6:
        risk_score += 5

    if features["num_hyphens"] > 3:
        risk_score += 5

    if features["num_dots"] > 4:
        risk_score += 5

    # Escalation
    if high_severity_count >= 2:
        risk_score *= 1.2

    # Critical override
    if features["has_ip"] and features["suspicious_keyword"]:
        risk_score = max(risk_score, 75)

    return min(int(risk_score), 100)