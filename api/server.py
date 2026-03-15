from pathlib import Path
import joblib
import pandas as pd
from fastapi import FastAPI

BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "model" / "api_attack_model.pkl"

app = FastAPI(title="Cloud API Attack Detection")

model = joblib.load(MODEL_PATH)

@app.get("/")
def home():
    return {"message": "API Attack Detection System Running"}

@app.post("/detect")
def detect_attack(
    requests_per_ip: int,
    failed_requests: int,
    unique_endpoints: int,
    avg_bytes: float
):
    data = pd.DataFrame(
        [[requests_per_ip, failed_requests, unique_endpoints, avg_bytes]],
        columns=[
            "requests_per_ip",
            "failed_requests",
            "unique_endpoints",
            "avg_bytes"
        ]
    )

    prediction = model.predict(data)[0]

    if prediction == -1:
        return {
            "status": "ALERT",
            "message": "Suspicious API activity detected"
        }

    return {
        "status": "OK",
        "message": "Normal API behaviour"
    }