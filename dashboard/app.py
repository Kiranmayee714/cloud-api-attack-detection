import streamlit as st
import pandas as pd
import os

st.set_page_config(
    page_title="Cloud API Attack Detection Dashboard",
    layout="wide"
)

st.title("Cloud API Attack Detection System")
st.subheader("Real-Time Security Monitoring Dashboard")

REQUESTS_FILE = "data/live_requests.csv"
FEATURES_FILE = "data/live_features.csv"
PREDICTIONS_FILE = "data/live_predictions.csv"
ALERTS_FILE = "data/alerts.csv"
BLOCKED_IPS_FILE = "data/blocked_ips.csv"


def load_csv(file_path):
    if os.path.exists(file_path):
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            st.warning(f"Could not read {file_path}: {e}")
            return pd.DataFrame()
    return pd.DataFrame()


requests_df = load_csv(REQUESTS_FILE)
features_df = load_csv(FEATURES_FILE)
predictions_df = load_csv(PREDICTIONS_FILE)
alerts_df = load_csv(ALERTS_FILE)
blocked_df = load_csv(BLOCKED_IPS_FILE)

total_requests = len(requests_df) if not requests_df.empty else 0
unique_ips = requests_df["client_ip"].nunique() if not requests_df.empty and "client_ip" in requests_df.columns else 0
suspicious_count = 0
blocked_count = 0

if not predictions_df.empty and "label" in predictions_df.columns:
    suspicious_count = (predictions_df["label"] == "Suspicious").sum()

if not blocked_df.empty and "client_ip" in blocked_df.columns:
    blocked_count = blocked_df["client_ip"].nunique()

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Requests", total_requests)
col2.metric("Unique IPs", unique_ips)
col3.metric("Suspicious IPs", suspicious_count)
col4.metric("Blocked IPs", blocked_count)

st.divider()

if not requests_df.empty:
    st.subheader("Live Request Logs")
    st.dataframe(requests_df, use_container_width=True)
else:
    st.info("No request logs available yet.")

if not features_df.empty:
    st.subheader("Extracted Features")
    st.dataframe(features_df, use_container_width=True)
else:
    st.info("No extracted features available yet.")

if not predictions_df.empty:
    st.subheader("Latest Predictions")
    st.dataframe(predictions_df, use_container_width=True)
else:
    st.info("No predictions available yet.")

if not alerts_df.empty:
    st.subheader("Alert History")
    st.dataframe(alerts_df, use_container_width=True)
else:
    st.info("No alerts generated yet.")

if not blocked_df.empty:
    st.subheader("Blocked IPs")
    st.dataframe(blocked_df, use_container_width=True)
else:
    st.info("No blocked IPs yet.")

st.divider()

if not requests_df.empty and "endpoint" in requests_df.columns:
    st.subheader("Endpoint Access Count")
    endpoint_counts = requests_df["endpoint"].value_counts().reset_index()
    endpoint_counts.columns = ["endpoint", "count"]
    st.bar_chart(endpoint_counts.set_index("endpoint"))

if not requests_df.empty and "client_ip" in requests_df.columns:
    st.subheader("Requests Per IP")
    ip_counts = requests_df["client_ip"].value_counts().reset_index()
    ip_counts.columns = ["client_ip", "count"]
    st.bar_chart(ip_counts.set_index("client_ip"))