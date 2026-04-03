# Cloud API Attack Detection System

## Project Overview

The **Cloud API Attack Detection System** is a real-time intelligent security solution designed to monitor API traffic, detect suspicious behavior using Machine Learning, generate alerts, simulate blocking, and visualize system activity through a dashboard.

Unlike static log analysis projects, this system works on **live API requests** and performs a complete end-to-end detection pipeline.

---

## Objective

The main goal of this project is to build a live API security monitoring system that can:

- Monitor incoming API traffic
- Log request behavior automatically
- Extract security-relevant features
- Detect anomalies using an ML model
- Generate alerts for suspicious activity
- Simulate blocking of malicious IP addresses
- Display results through a Streamlit dashboard

---

## Problem Statement

Modern APIs are often exposed to abnormal traffic patterns such as:

- brute force attempts
- endpoint probing
- scraping
- unusual request bursts
- suspicious access behavior

Traditional dashboards only visualize logs after the fact.  
This project focuses on **real-time detection and response** using a machine learning-based anomaly detection pipeline.

---

## Key Features

- Real-time API traffic monitoring
- Automatic request logging using FastAPI middleware
- Feature extraction from live request logs
- Machine learning-based anomaly detection using Isolation Forest
- Alert generation for suspicious IPs
- Simulated IP blocking mechanism
- Interactive Streamlit dashboard for monitoring

---

## Tech Stack

- **Backend:** FastAPI
- **Dashboard:** Streamlit
- **Machine Learning:** Scikit-learn (Isolation Forest)
- **Language:** Python
- **Data Processing:** Pandas
- **Model Storage:** Joblib

---

## Project Structure

```text
cloud-api-attack-detection/
│
├── api/
│   └── server.py
│
├── dashboard/
│   └── app.py
│
├── data/
│   ├── live_requests.csv
│   ├── live_features.csv
│   ├── live_predictions.csv
│   ├── alerts.csv
│   ├── blocked_ips.csv
│   ├── access.log
│   ├── api_logs.csv
│   └── api_features.csv
│
├── ml/
│   ├── parse_logs.py
│   ├── feature_engineering.py
│   ├── train_model.py
│   ├── realtime_features.py
│   ├── realtime_predict.py
│   └── alert_engine.py
│
├── model/
│   └── api_attack_model.pkl
│
├── requirements.txt
└── README.md

System Workflow
User Request
→ FastAPI API Endpoint
→ Middleware Logging
→ live_requests.csv
→ Real-Time Feature Extraction
→ live_features.csv
→ Isolation Forest Prediction
→ live_predictions.csv
→ Alert Generation
→ alerts.csv
→ Block Simulation
→ blocked_ips.csv
→ Streamlit Dashboard


Installation
1. Clone the repository
git clone <your-repository-link>
cd cloud-api-attack-detection
2. Create virtual environment
python -m venv venv
3. Activate environment
Windows
venv\Scripts\activate
Linux/Mac
source venv/bin/activate
4. Install dependencies
pip install -r requirements.txt
Running the Project
Start FastAPI server
uvicorn api.server:app --reload

FastAPI runs on:

http://127.0.0.1:8000
Start Streamlit dashboard
streamlit run dashboard/app.py
Testing the System
1. Access API endpoints

Open these in browser or Postman:

http://127.0.0.1:8000/
http://127.0.0.1:8000/login
http://127.0.0.1:8000/data
http://127.0.0.1:8000/admin
http://127.0.0.1:8000/health
2. Trigger pipeline

For localhost/demo testing:

http://127.0.0.1:8000/test-pipeline
3. Refresh dashboard

Open Streamlit dashboard and refresh to see:

live logs
extracted features
predictions
alerts
blocked IPs