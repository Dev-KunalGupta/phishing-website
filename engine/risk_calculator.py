def calculate_final_risk(ml_probability, rule_score, features,
                         ml_weight=0.6, rule_weight=0.4):

    ml_score = ml_probability * 100

    # Reputation Dampening
    if (
        features.get("is_popular_domain", 0) == 1 and
        rule_score == 0 and
        features.get("has_https", 0) == 1 and
        ml_probability < 0.85
    ):
        ml_weight = 0.2
        rule_weight = 0.8

    final_risk = (ml_weight * ml_score) + (rule_weight * rule_score)

    # Critical Override
    if features.get("has_ip", 0) and features.get("suspicious_keyword", 0):
        final_risk = max(final_risk, 75)

    final_risk = max(0, min(final_risk, 100))

    # Classification
    if final_risk <= 30:
        classification = "Safe"
    elif final_risk <= 70:
        classification = "Suspicious"
    else:
        classification = "Phishing"

    # Improved Confidence
    confidence = abs(ml_probability - 0.5) * 200

    if rule_score >= 60:
        confidence = max(confidence, 70)

    confidence = min(confidence, 100)

    return {
        "final_risk": round(float(final_risk), 2),
        "classification": classification,
        "confidence": round(float(confidence), 2)
    }
