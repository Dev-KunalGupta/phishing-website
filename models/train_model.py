import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from xgboost import XGBClassifier

DATA_FILE = "models/training_data.csv"
MODEL_FILE = "models/phishing_model.pkl"

def train():

    print("Loading dataset...")
    df = pd.read_csv(DATA_FILE)

    # Separate features and label
    X = df.drop("label", axis=1)
    y = df["label"]

    print("Splitting dataset...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    print("Training XGBoost model...")
    model = XGBClassifier(
        n_estimators=200,
        max_depth=5,
        learning_rate=0.1,
        use_label_encoder=False,
        eval_metric="logloss"
    )

    model.fit(X_train, y_train)

    print("Evaluating model...")
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)

    print("Accuracy:", accuracy)
    print("\nClassification Report:\n")
    print(classification_report(y_test, y_pred))

    print("Saving model...")
    joblib.dump(model, MODEL_FILE)

    print("Model saved to:", MODEL_FILE)

if __name__ == "__main__":
    train()
