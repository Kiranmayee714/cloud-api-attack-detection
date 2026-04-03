import os
import pandas as pd
import joblib
import numpy as np
from sklearn.ensemble import IsolationForest

INPUT_FILE = "data/api_features_v2.csv"
MODEL_FILE = "model/api_attack_model.pkl"

def train_model():
    if not os.path.exists(INPUT_FILE):
        print(f"Training file not found: {INPUT_FILE}")
        return

    df = pd.read_csv(INPUT_FILE)

    if df.empty:
        print("Training dataset is empty.")
        return

    expected_columns = [
        "client_ip",
        "requests_per_ip",
        "failed_requests",
        "unique_endpoints",
        "avg_bytes",
        "avg_response_time",
        "admin_access_count",
        "failure_rate",
        "request_rate_per_min"
    ]

    missing = [col for col in expected_columns if col not in df.columns]
    if missing:
        print(f"Missing columns in training file: {missing}")
        return

    X = df[
        [
            "requests_per_ip",
            "failed_requests",
            "unique_endpoints",
            "avg_bytes",
            "avg_response_time",
            "admin_access_count",
            "failure_rate",
            "request_rate_per_min"
        ]
    ].copy()

    for col in X.columns:
        X[col] = pd.to_numeric(X[col], errors="coerce")

    X = X.fillna(0)

    model = IsolationForest(
        n_estimators=100,
        contamination=0.05,
        random_state=42
    )

    model.fit(X)

    os.makedirs("model", exist_ok=True)
    joblib.dump(model, MODEL_FILE)

    print("Model trained successfully!")
    print(f"Model saved to: {MODEL_FILE}")

    predictions = model.predict(X)
    df["anomaly"] = predictions

    print("\nPrediction sample:")
    print(df.head())

    anomaly_count = np.sum(predictions == -1)
    normal_count = np.sum(predictions == 1)

    print("\nModel Evaluation:")
    print("Normal behaviour detected:", normal_count)
    print("Suspicious behaviour detected:", anomaly_count)

if __name__ == "__main__":
    train_model()