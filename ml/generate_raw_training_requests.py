import os
import random
import pandas as pd
from datetime import datetime, timedelta

OUTPUT_FILE = "data/training_requests_raw.csv"

NORMAL_ENDPOINTS = ["/", "/login", "/data", "/health"]
SUSPICIOUS_ENDPOINTS = ["/admin", "/admin", "/admin", "/secret", "/config", "/debug", "/login"]

def random_ip():
    return f"192.168.1.{random.randint(2, 200)}"

def generate_normal_rows(start_time, count=500):
    rows = []
    for _ in range(count):
        timestamp = start_time + timedelta(seconds=random.randint(0, 3600))
        endpoint = random.choice(NORMAL_ENDPOINTS)
        status_code = random.choice([200, 200, 200, 200, 404])
        response_time_ms = round(random.uniform(0.5, 3.0), 2)
        payload_size = random.choice([0, 64, 128, 256, 512])

        rows.append([
            timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            random_ip(),
            "GET",
            endpoint,
            status_code,
            response_time_ms,
            payload_size,
            "NormalAgent/1.0"
        ])
    return rows

def generate_suspicious_rows(start_time, count=200):
    rows = []
    for _ in range(count):
        timestamp = start_time + timedelta(seconds=random.randint(0, 3600))
        endpoint = random.choice(SUSPICIOUS_ENDPOINTS)
        status_code = random.choice([200, 401, 403, 404, 500])
        response_time_ms = round(random.uniform(2.0, 15.0), 2)
        payload_size = random.choice([0, 512, 1024, 2048, 4096])

        rows.append([
            timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            random_ip(),
            "GET",
            endpoint,
            status_code,
            response_time_ms,
            payload_size,
            "AttackSimulator/1.0"
        ])
    return rows

def main():
    os.makedirs("data", exist_ok=True)

    start_time = datetime.now()

    rows = []
    rows.extend(generate_normal_rows(start_time, 500))
    rows.extend(generate_suspicious_rows(start_time, 200))

    df = pd.DataFrame(rows, columns=[
        "timestamp",
        "client_ip",
        "method",
        "endpoint",
        "status_code",
        "response_time_ms",
        "payload_size",
        "user_agent"
    ])

    df = df.sort_values("timestamp")
    df.to_csv(OUTPUT_FILE, index=False)

    print(f"Raw training request data saved to {OUTPUT_FILE}")
    print(df.head())

if __name__ == "__main__":
    main()