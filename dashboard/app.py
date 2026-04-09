import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="Cloud API Attack Detection Dashboard", layout="wide")

st.title("Cloud API Attack Detection System")
st.subheader("Real-Time Security Monitoring Dashboard")

BASE_URL = "https://cloud-api-attack-detection.onrender.com"


@st.cache_data(ttl=15)
def fetch_data(endpoint, key):
    try:
        response = requests.get(f"{BASE_URL}{endpoint}", timeout=15)
        if response.status_code == 200:
            data = response.json()
            return pd.DataFrame(data.get(key, []))
        return pd.DataFrame()
    except Exception:
        return pd.DataFrame()


logs_df = fetch_data("/logs", "logs")
predictions_df = fetch_data("/predictions", "predictions")
alerts_df = fetch_data("/alerts", "alerts")
blocked_df = fetch_data("/blocked-ips", "blocked_ips")

total_requests = len(logs_df) if not logs_df.empty else 0
unique_ips = logs_df["client_ip"].nunique() if not logs_df.empty and "client_ip" in logs_df.columns else 0
suspicious_count = (predictions_df["label"] == "Suspicious").sum() if not predictions_df.empty and "label" in predictions_df.columns else 0
blocked_count = blocked_df["client_ip"].nunique() if not blocked_df.empty and "client_ip" in blocked_df.columns else 0

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Requests", total_requests)
col2.metric("Unique IPs", unique_ips)
col3.metric("Suspicious IPs", suspicious_count)
col4.metric("Blocked IPs", blocked_count)

st.divider()

if not logs_df.empty:
    st.subheader("Live Request Logs")
    st.dataframe(logs_df, use_container_width=True)
else:
    st.info("No request logs available yet.")

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

if not logs_df.empty and "endpoint" in logs_df.columns:
    st.subheader("Endpoint Access Count")
    endpoint_counts = logs_df["endpoint"].value_counts().reset_index()
    endpoint_counts.columns = ["endpoint", "count"]
    st.bar_chart(endpoint_counts.set_index("endpoint"))

if not logs_df.empty and "client_ip" in logs_df.columns:
    st.subheader("Requests Per IP")
    ip_counts = logs_df["client_ip"].value_counts().reset_index()
    ip_counts.columns = ["client_ip", "count"]
    st.bar_chart(ip_counts.set_index("client_ip"))