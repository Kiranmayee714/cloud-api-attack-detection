import os
import pandas as pd
import joblib

FEATURES_FILE = "data/live_features.csv"
MODEL_FILE = "model/api_attack_model.pkl"
OUTPUT_FILE = "data/live_predictions.csv"

def run_realtime_prediction():
    if not os.path.exists(FEATURES_FILE):
        print(f"Features file not found: {FEATURES_FILE}")
        return

    if not os.path.exists(MODEL_FILE):
        print(f"Model file not found: {MODEL_FILE}")
        return

    df = pd.read_csv(FEATURES_FILE)

    if df.empty:
        print("No live features available for prediction.")
        return

    expected_columns = [
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
        print(f"Missing columns in live features file: {missing}")
        return

    X = df[expected_columns].copy()

    for col in X.columns:
        X[col] = pd.to_numeric(X[col], errors="coerce")

    X = X.fillna(0)

    model = joblib.load(MODEL_FILE)

    df["prediction"] = model.predict(X)
    df["label"] = df["prediction"].map({1: "Normal", -1: "Suspicious"})

    if hasattr(model, "decision_function"):
        df["anomaly_score"] = model.decision_function(X).round(4)

    df.to_csv(OUTPUT_FILE, index=False)

    print("Real-time predictions generated successfully.")
    print(df.head())

if __name__ == "__main__":
    run_realtime_prediction()