from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import time
import csv
import os
import sys
import subprocess
from datetime import datetime
import pandas as pd

app = FastAPI(title="Cloud API Attack Detection System")

LOG_FILE = "data/live_requests.csv"
BLOCKED_IPS_FILE = "data/blocked_ips.csv"
PREDICTIONS_FILE = "data/live_predictions.csv"
ALERTS_FILE = "data/alerts.csv"

LOG_HEADERS = [
    "timestamp",
    "client_ip",
    "method",
    "endpoint",
    "status_code",
    "response_time_ms",
    "payload_size",
    "user_agent"
]

ON_RENDER = os.getenv("RENDER") == "true"
DISABLE_BLOCKING = True if ON_RENDER else False


def ensure_data_folder():
    os.makedirs("data", exist_ok=True)


def ensure_log_file():
    ensure_data_folder()
    if not os.path.exists(LOG_FILE) or os.path.getsize(LOG_FILE) == 0:
        with open(LOG_FILE, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(LOG_HEADERS)


def ensure_blocked_ips_file():
    ensure_data_folder()
    if not os.path.exists(BLOCKED_IPS_FILE) or os.path.getsize(BLOCKED_IPS_FILE) == 0:
        with open(BLOCKED_IPS_FILE, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["client_ip", "blocked_at", "reason"])


def get_client_ip(request: Request) -> str:
    forwarded_for = request.headers.get("x-forwarded-for")
    if forwarded_for:
        return forwarded_for.split(",")[0].strip()

    real_ip = request.headers.get("x-real-ip")
    if real_ip:
        return real_ip.strip()

    if request.client and request.client.host:
        return request.client.host

    return "unknown"


def is_ip_blocked(client_ip: str) -> bool:
    if not os.path.exists(BLOCKED_IPS_FILE):
        return False

    try:
        blocked_df = pd.read_csv(BLOCKED_IPS_FILE)
        if blocked_df.empty or "client_ip" not in blocked_df.columns:
            return False
        blocked_ips = blocked_df["client_ip"].astype(str).tolist()
        return client_ip in blocked_ips
    except Exception:
        return False


def trigger_pipeline():
    scripts = [
        "ml/realtime_features.py",
        "ml/realtime_predict.py",
        "ml/alert_engine.py"
    ]

    for script in scripts:
        try:
            subprocess.run(
                [sys.executable, script],
                check=False,
                capture_output=True,
                text=True,
                timeout=20
            )
        except Exception as e:
            print(f"Error running {script}: {e}")


ensure_log_file()
ensure_blocked_ips_file()


@app.middleware("http")
async def security_middleware(request: Request, call_next):
    ensure_log_file()
    ensure_blocked_ips_file()

    client_ip = get_client_ip(request)
    endpoint = request.url.path

    excluded_paths = {
        "/",
        "/health",
        "/logs",
        "/predictions",
        "/alerts",
        "/blocked-ips",
        "/docs",
        "/openapi.json",
        "/favicon.ico",
        "/test-pipeline"
    }

    if not DISABLE_BLOCKING:
        if client_ip != "127.0.0.1" and is_ip_blocked(client_ip):
            return JSONResponse(
                status_code=403,
                content={"message": f"Access denied for blocked IP: {client_ip}"}
            )

    start_time = time.time()

    try:
        response = await call_next(request)
        status_code = response.status_code
    except Exception:
        status_code = 500
        raise
    finally:
        process_time = round((time.time() - start_time) * 1000, 2)
        method = request.method
        payload_size = request.headers.get("content-length", 0)
        user_agent = request.headers.get("user-agent", "unknown")
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with open(LOG_FILE, mode="a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow([
                timestamp,
                client_ip,
                method,
                endpoint,
                status_code,
                process_time,
                payload_size,
                user_agent
            ])

        # IMPORTANT: do NOT run pipeline for dashboard/API read routes
        if client_ip != "127.0.0.1" and endpoint not in excluded_paths:
            trigger_pipeline()

    return response


@app.api_route("/", methods=["GET", "HEAD"])
def home():
    return {"message": "API Attack Detection System is running"}


@app.get("/login")
def login():
    return {"message": "Login endpoint accessed"}


@app.get("/data")
def get_data():
    return {"message": "Data fetched successfully"}


@app.get("/admin")
def admin_panel():
    return {"message": "Admin panel accessed"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.get("/test-pipeline")
def test_pipeline():
    trigger_pipeline()
    return {"message": "Pipeline executed successfully"}


@app.get("/logs")
def get_logs():
    if not os.path.exists(LOG_FILE):
        return {"logs": []}

    try:
        df = pd.read_csv(LOG_FILE)
        return {"logs": df.tail(50).to_dict(orient="records")}
    except Exception as e:
        return {"logs": [], "error": str(e)}


@app.get("/predictions")
def get_predictions():
    if not os.path.exists(PREDICTIONS_FILE):
        return {"predictions": []}

    try:
        df = pd.read_csv(PREDICTIONS_FILE)
        return {"predictions": df.to_dict(orient="records")}
    except Exception as e:
        return {"predictions": [], "error": str(e)}


@app.get("/alerts")
def get_alerts():
    if not os.path.exists(ALERTS_FILE):
        return {"alerts": []}

    try:
        df = pd.read_csv(ALERTS_FILE)
        return {"alerts": df.to_dict(orient="records")}
    except Exception as e:
        return {"alerts": [], "error": str(e)}


@app.get("/blocked-ips")
def get_blocked_ips():
    if not os.path.exists(BLOCKED_IPS_FILE):
        return {"blocked_ips": []}

    try:
        df = pd.read_csv(BLOCKED_IPS_FILE)
        return {"blocked_ips": df.to_dict(orient="records")}
    except Exception as e:
        return {"blocked_ips": [], "error": str(e)}


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error"}
    )