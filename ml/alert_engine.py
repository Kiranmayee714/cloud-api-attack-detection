import pandas as pd
import os
from datetime import datetime

from api.alerting import send_alert_email

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

    # Send email alerts for suspicious rows
    for _, row in suspicious_df.iterrows():
        subject = "API Attack Alert Detected"
        body = (
            f"Suspicious API activity detected.\n\n"
            f"Time: {row['alert_time']}\n"
            f"Client IP: {row['client_ip']}\n"
            f"Requests per IP: {row['requests_per_ip']}\n"
            f"Failed Requests: {row['failed_requests']}\n"
            f"Unique Endpoints: {row['unique_endpoints']}\n"
            f"Average Bytes: {row['avg_bytes']}\n"
            f"Prediction: {row['prediction']}\n"
            f"Label: {row['label']}\n"
            f"Anomaly Score: {row['anomaly_score']}\n"
            f"Action: BLOCK_SIMULATED\n"
        )
        send_alert_email(subject, body)

    print("Alert generated successfully.")
    print(alerts_to_save.tail())
    print("\nBlocked IPs:")
    print(blocked_ips)


if __name__ == "__main__":
    process_alerts()