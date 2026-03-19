from engine.feature_extractor import extract_url_features
from engine.rule_engine import calculate_rule_risk
from engine.ml_detector import predict_ml_probability
from engine.risk_calculator import calculate_final_risk
from engine.explanation_engine import generate_explanation

url = "https://mail.google.com"


# Step 1: Extract features
features = extract_url_features(url)

# Step 2: ML probability
ml_prob = predict_ml_probability(features)

# Step 3: Rule score
rule_score = calculate_rule_risk(features)

# Step 4: Final risk
result = calculate_final_risk(
    ml_probability=ml_prob,
    rule_score=rule_score,
    features=features
)

# Step 5: Explanation
explanation = generate_explanation(
    features,
    rule_score,
    result["final_risk"],
    result["classification"]
)

print("ML Probability:", ml_prob)
print("Rule Score:", rule_score)
print("Final Result:", result)
print("Explanation:", explanation)
