import pandas as pd
import os
from datetime import datetime

PREDICTIONS_FILE = "data/live_predictions.csv"
ALERTS_FILE = "data/alerts.csv"
BLOCKED_IPS_FILE = "data/blocked_ips.csv"

def process_alerts():
    if not os.path.exists(PREDICTIONS_FILE):
        print(f"Predictions file not found: {PREDICTIONS_FILE}")
        return

    df = pd.read_csv(PREDICTIONS_FILE)

    if df.empty:
        print("No predictions available.")
        return

    suspicious_df = df[df["label"] == "Suspicious"].copy()

    if suspicious_df.empty:
        print("No suspicious activity detected.")
        return

    suspicious_df["alert_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    suspicious_df["alert_message"] = suspicious_df.apply(
        lambda row: f"Suspicious activity detected from IP {row['client_ip']}",
        axis=1
    )
    suspicious_df["action"] = "BLOCK_SIMULATED"

    alert_columns = [
        "alert_time",
        "client_ip",
        "requests_per_ip",
        "failed_requests",
        "unique_endpoints",
        "avg_bytes",
        "prediction",
        "label",
        "anomaly_score",
        "alert_message",
        "action"
    ]

    alerts_to_save = suspicious_df[alert_columns]

    if os.path.exists(ALERTS_FILE):
        existing_alerts = pd.read_csv(ALERTS_FILE)
        alerts_to_save = pd.concat([existing_alerts, alerts_to_save], ignore_index=True)

    alerts_to_save.to_csv(ALERTS_FILE, index=False)

    blocked_ips = suspicious_df[["client_ip"]].drop_duplicates().copy()
    blocked_ips["blocked_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    blocked_ips["reason"] = "ML anomaly detection"

    if os.path.exists(BLOCKED_IPS_FILE):
        existing_blocked = pd.read_csv(BLOCKED_IPS_FILE)
        blocked_ips = pd.concat([existing_blocked, blocked_ips], ignore_index=True)
        blocked_ips = blocked_ips.drop_duplicates(subset=["client_ip"], keep="last")

    blocked_ips.to_csv(BLOCKED_IPS_FILE, index=False)

    print("Alert generated successfully.")
    print(alerts_to_save.tail())
    print("\nBlocked IPs:")
    print(blocked_ips)

if __name__ == "__main__":
    process_alerts()
    