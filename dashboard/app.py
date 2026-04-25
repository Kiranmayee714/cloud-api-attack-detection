import streamlit as st
import pandas as pd
import os
import time

st.title("Cloud API Attack Detection Dashboard")

LIVE_LOG_FILE = "data/live_requests.csv"
ALERTS_FILE = "data/alerts.csv"
BLOCKED_IPS_FILE = "data/blocked_ips.csv"

st.subheader("Kafka-like Live Stream Events")

placeholder = st.empty()

if os.path.exists(LIVE_LOG_FILE):
    df = pd.read_csv(LIVE_LOG_FILE)

    with placeholder.container():
        st.metric("Total Stream Events", len(df))

        if "endpoint" in df.columns:
            st.subheader("Endpoint Traffic")
            st.bar_chart(df["endpoint"].value_counts())

        if "status_code" in df.columns:
            st.subheader("Status Code Distribution")
            st.bar_chart(df["status_code"].value_counts())

        st.subheader("Latest Stream Events")
        st.dataframe(df.tail(20))
else:
    st.warning("No live stream data found yet.")