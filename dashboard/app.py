from pathlib import Path
import streamlit as st
import pandas as pd
import joblib

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "api_features.csv"
MODEL_PATH = BASE_DIR / "model" / "api_attack_model.pkl"

st.title("Cloud API Attack Detection Dashboard")

df = pd.read_csv(DATA_PATH)
model = joblib.load(MODEL_PATH)

X = df.drop("ip", axis=1)
df["anomaly"] = model.predict(X)

st.subheader("API Traffic Dataset")
st.dataframe(df.head(20))

attack_count = (df["anomaly"] == -1).sum()
normal_count = (df["anomaly"] == 1).sum()

st.subheader("Anomaly Detection Results")
st.write("Normal Requests:", int(normal_count))
st.write("Suspicious Requests:", int(attack_count))

st.subheader("Requests per IP")
st.bar_chart(df["requests_per_ip"])

st.subheader("Unique Endpoints Accessed")
st.bar_chart(df["unique_endpoints"])

st.subheader("Payload Size Distribution")
st.line_chart(df["avg_bytes"])