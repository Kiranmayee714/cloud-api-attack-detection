import os
import pandas as pd

INPUT_FILE = "data/training_requests_raw.csv"
OUTPUT_FILE = "data/api_features_v2.csv"

def build_features():
    if not os.path.exists(INPUT_FILE):
        print(f"Input file not found: {INPUT_FILE}")
        return

    df = pd.read_csv(INPUT_FILE)

    if df.empty:
        print("Input data is empty.")
        return

    required_cols = ["timestamp", "client_ip", "endpoint", "status_code", "payload_size", "response_time_ms"]
    missing = [col for col in required_cols if col not in df.columns]

    if missing:
        print(f"Missing required columns: {missing}")
        return

    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
    df["status_code"] = pd.to_numeric(df["status_code"], errors="coerce").fillna(0)
    df["payload_size"] = pd.to_numeric(df["payload_size"], errors="coerce").fillna(0)
    df["response_time_ms"] = pd.to_numeric(df["response_time_ms"], errors="coerce").fillna(0)

    features = df.groupby("client_ip").agg(
        requests_per_ip=("client_ip", "count"),
        failed_requests=("status_code", lambda x: (x >= 400).sum()),
        unique_endpoints=("endpoint", "nunique"),
        avg_bytes=("payload_size", "mean"),
        avg_response_time=("response_time_ms", "mean"),
        admin_access_count=("endpoint", lambda x: (x == "/admin").sum())
    ).reset_index()

    features["failure_rate"] = (
        features["failed_requests"] / features["requests_per_ip"]
    ).fillna(0)

    def calc_rate(group):
        tmin = group["timestamp"].min()
        tmax = group["timestamp"].max()
        if pd.isna(tmin) or pd.isna(tmax):
            return 0
        minutes = max((tmax - tmin).total_seconds() / 60, 1)
        return round(len(group) / minutes, 2)

    rate_df = df.groupby("client_ip").apply(calc_rate).reset_index(name="request_rate_per_min")

    features = features.merge(rate_df, on="client_ip", how="left")

    features["avg_bytes"] = features["avg_bytes"].round(2)
    features["avg_response_time"] = features["avg_response_time"].round(2)
    features["failure_rate"] = features["failure_rate"].round(3)

    features.to_csv(OUTPUT_FILE, index=False)

    print(f"Rich training features saved to {OUTPUT_FILE}")
    print(features.head())

if __name__ == "__main__":
    build_features()