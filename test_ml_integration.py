from engine.feature_extractor import extract_url_features
from engine.ml_detector import predict_ml_probability

url = "http://192.168.0.1/login"

features = extract_url_features(url)

prob = predict_ml_probability(features)

print("ML Probability:", prob)
