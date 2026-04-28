import joblib
import pandas as pd

MODEL_PATH = "models/phishing_model.pkl"

# Load model once
model = joblib.load(MODEL_PATH)

def predict_ml_probability(features_dict):
    """
    Takes feature dictionary and returns phishing probability (0 to 1)
    """

    # Convert dictionary to DataFrame (model expects tabular input)
    df = pd.DataFrame([features_dict])

    # Predict probability
    probability = model.predict_proba(df)[0][1]

    return probability
