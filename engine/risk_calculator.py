# def calculate_final_risk(ml_probability, rule_score, features,
#                          ml_weight=0.5, rule_weight=0.5):

#     ml_score = ml_probability * 100

#     is_popular = features.get("is_popular_domain", 0)
#     has_https = features.get("has_https", 0)

#     # STRONG REPUTATION PROTECTION
#     if is_popular == 1 and has_https == 1:
#         ml_weight = 0.3
#         rule_weight = 0.2

#     # STRONG SUSPICIOUS BOOST
#     if features.get("has_ip", 0):
#         ml_weight = 0.4
#         rule_weight = 0.6

#     final_risk = (ml_weight * ml_score) + (rule_weight * rule_score)

#     # Critical override
#     if features.get("has_ip", 0) and features.get("suspicious_keyword", 0):
#         final_risk = max(final_risk, 75)

#     final_risk = max(0, min(final_risk, 100))

#     # BETTER CLASSIFICATION
#     if final_risk <= 35:
#         classification = "Safe"
#     elif final_risk <= 65:
#         classification = "Suspicious"
#     else:
#         classification = "Phishing"

#     # Confidence
#     confidence = abs(ml_probability - 0.5) * 200

#     if rule_score >= 60:
#         confidence = max(confidence, 75)

#     confidence = min(confidence, 100)

#     return {
#         "final_risk": round(float(final_risk), 2),
#         "classification": classification,
#         "confidence": round(float(confidence), 2)
#     }



def calculate_final_risk(ml_probability, rule_score, features,
                         ml_weight=0.5, rule_weight=0.5):

    ml_score = ml_probability * 100

    is_popular = features.get("is_popular_domain", 0)
    has_https = features.get("has_https", 0)

    final_risk = (ml_weight * ml_score) + (rule_weight * rule_score)

    # CRITICAL OVERRIDE
    if features.get("has_ip", 0) and features.get("suspicious_keyword", 0):
        final_risk = max(final_risk, 75)

    # STRONG TRUST OVERRIDE
    if is_popular == 1 and has_https == 1:
        final_risk = min(final_risk, 25)

    # Clamp
    final_risk = max(0, min(final_risk, 100))

    # Classification
    if final_risk <= 30:
        classification = "Safe"
    elif final_risk <= 70:
        classification = "Suspicious"
    else:
        classification = "Phishing"

    # Confidence
    confidence = abs(ml_probability - 0.5) * 200

    if rule_score >= 60:
        confidence = max(confidence, 75)

    confidence = min(confidence, 100)

    return {
        "final_risk": round(float(final_risk), 2),
        "classification": classification,
        "confidence": round(float(confidence), 2)
    }