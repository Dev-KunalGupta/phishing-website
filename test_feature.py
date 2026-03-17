from engine.feature_extractor import extract_url_features
from engine.rule_engine import calculate_rule_risk
from engine.risk_calculator import calculate_final_risk
from engine.explanation_engine import generate_explanation

url = "http://192.168.0.1/login"

features = extract_url_features(url)
rule_score = calculate_rule_risk(features)

# Assume ML gives 0.4 probability (40%)
result = calculate_final_risk(
    ml_probability=0.4,
    rule_score=rule_score,
    features=features
)


explanation = generate_explanation(
    features,
    rule_score,
    result["final_risk"],
    result["classification"]
)

print("Final Risk:", result)
print("Explanation:", explanation)
