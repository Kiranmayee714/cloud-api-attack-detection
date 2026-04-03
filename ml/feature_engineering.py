import pandas as pd
import os

INPUT_FILE = "data/requests.csv"   # change if needed
OUTPUT_FILE = "data/training_features_v2.csv"

def build_training_features():
    df = pd.read_csv(INPUT_FILE)

    # If your file already aggregated (like yours)
    if "client_ip" not in df.columns:
        df.columns = [
            "client_ip",
            "requests_per_ip",
            "failed_requests",
            "unique_endpoints",
            "avg_bytes"
        ]

        # Add missing columns with simulated values (important)
        df["avg_response_time"] = df["avg_bytes"] / 10000
        df["admin_access_count"] = (df["unique_endpoints"] * 0.2).astype(int)

        df["failure_rate"] = (
            df["failed_requests"] / df["requests_per_ip"]
        ).fillna(0)

        df["request_rate_per_min"] = df["requests_per_ip"] / 5

        df = df.fillna(0)

    else:
        print("Already structured dataset")

    df.to_csv(OUTPUT_FILE, index=False)

    print("✅ Training features ready")
    print(df.head())


if __name__ == "__main__":
    build_training_features()