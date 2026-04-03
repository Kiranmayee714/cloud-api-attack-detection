import pandas as pd
import os

INPUT_FILE = "data/live_requests.csv"
OUTPUT_FILE = "data/live_features.csv"

def extract_realtime_features():
    if not os.path.exists(INPUT_FILE):
        print(f"Input file not found: {INPUT_FILE}")
        return

    df = pd.read_csv(INPUT_FILE)

    if df.empty:
        print("No request data available.")
        return

    # Convert columns
    df["status_code"] = pd.to_numeric(df["status_code"], errors="coerce").fillna(0)
    df["payload_size"] = pd.to_numeric(df["payload_size"], errors="coerce").fillna(0)
    df["response_time_ms"] = pd.to_numeric(df["response_time_ms"], errors="coerce").fillna(0)

    # Convert timestamp
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")

    # Group features
    features = df.groupby("client_ip").agg(
        requests_per_ip=("client_ip", "count"),
        failed_requests=("status_code", lambda x: (x >= 400).sum()),
        unique_endpoints=("endpoint", "nunique"),
        avg_bytes=("payload_size", "mean"),
        avg_response_time=("response_time_ms", "mean"),
        admin_access_count=("endpoint", lambda x: (x == "/admin").sum())
    ).reset_index()

    # Derived features
    features["failure_rate"] = (
        features["failed_requests"] / features["requests_per_ip"]
    ).round(3)

    # Request rate per minute
    time_span = df["timestamp"].max() - df["timestamp"].min()
    minutes = max(time_span.total_seconds() / 60, 1)

    features["request_rate_per_min"] = (
        features["requests_per_ip"] / minutes
    ).round(2)

    # Round values
    features["avg_bytes"] = features["avg_bytes"].round(2)
    features["avg_response_time"] = features["avg_response_time"].round(2)

    os.makedirs("data", exist_ok=True)
    features.to_csv(OUTPUT_FILE, index=False)

    print("Enhanced features extracted successfully.")
    print(features)

if __name__ == "__main__":
    extract_realtime_features()