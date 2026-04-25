# 🚀 Cloud API Attack Detection System

A real-time API monitoring and anomaly detection system that identifies suspicious behavior in API traffic using Machine Learning, generates alerts, and notifies administrators via email.

---

## 📌 Overview

Modern applications rely heavily on APIs, making them a major attack surface. This project implements a **real-time API attack detection pipeline** that:

* Monitors live API requests
* Extracts behavioral features
* Detects anomalies using Machine Learning
* Generates alerts and simulates IP blocking
* Sends email notifications to administrators
* Visualizes activity through a dashboard

---

## ⚙️ Features

* 🔍 **Real-time API request monitoring**
* 📊 **Feature extraction from API traffic**
* 🤖 **Anomaly detection using Isolation Forest**
* 🚨 **Automatic alert generation**
* 📩 **Email notifications for suspicious activity**
* ⛔ **Simulated IP blocking**
* 📈 **Streamlit dashboard for visualization**
* 🐳 **Dockerized deployment**

---

## 🏗️ System Architecture

```text
User Request
   │
   ▼
FastAPI Backend (API Endpoints)
   │
   ▼
Request Logging Middleware
   │
   ▼
Live Data Storage (CSV)
   │
   ▼
Feature Engineering (Per IP)
   │
   ▼
ML Model (Isolation Forest)
   │
   ▼
Prediction (Normal / Suspicious)
   │
   ▼
Alert Engine
   │
   ├── Alerts Stored
   ├── Blocked IPs Updated
   └── Email Notification Sent
   │
   ▼
Dashboard (Streamlit)
```

---

## 🧠 Machine Learning Model

* Model: **Isolation Forest**
* Type: Unsupervised anomaly detection
* Detects unusual patterns in:

  * Requests per IP
  * Failed requests
  * Unique endpoints accessed
  * Payload size behavior

---

## 📂 Project Structure

```text
cloud-api-attack-detection/
│
├── api/
│   ├── server.py          # FastAPI application
│   ├── middleware.py      # Request logging middleware
│   └── alerting.py        # Email alert system
│
├── ml/
│   ├── parse_logs.py
│   ├── feature_engineering.py
│   ├── realtime_features.py
│   ├── realtime_predict.py
│   ├── alert_engine.py
│   └── train_model.py
│
├── dashboard/
│   └── app.py             # Streamlit dashboard
│
├── model/
│   └── api_attack_model.pkl
│
├── data/                  # Runtime generated files (ignored in git)
│
├── Dockerfile
├── .dockerignore
├── .gitignore
├── requirements.txt
└── README.md
```

---

## 🚀 How to Run Locally

### 1️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

---

### 2️⃣ Run FastAPI server

```bash
uvicorn api.server:app --reload
```

Open:

```text
http://127.0.0.1:8000/docs
```

---

### 3️⃣ Run Dashboard

```bash
streamlit run dashboard/app.py
```

---

## 🐳 Run with Docker

### Build image

```bash
docker build -t api-attack-detection .
```

### Run container

```bash
docker run -p 8000:8000 api-attack-detection
```

---

## 📩 Email Alert Setup

Create a `.env` file:

```env
EMAIL_SENDER=yourgmail@gmail.com
EMAIL_PASSWORD=your_app_password
EMAIL_RECEIVER=yourgmail@gmail.com
```

⚠️ Use **Gmail App Password**, not your actual password.

---

## 🔍 How It Works

1. User sends API request
2. Middleware logs request data
3. Features are generated per IP
4. ML model predicts anomaly
5. If suspicious:

   * Alert is generated
   * IP is marked as blocked (simulated)
   * Email notification is sent
6. Dashboard displays system activity

---

## 📊 Sample Outputs

* Alerts stored in `alerts.csv`
* Blocked IPs stored in `blocked_ips.csv`
* Live monitoring via dashboard
* Email notifications on detection

---

## 🎯 Use Cases

* API security monitoring
* Intrusion detection systems
* Cloud-native security pipelines
* DevOps observability systems

---

## 🛠️ Tech Stack

* **Backend:** FastAPI
* **ML:** Scikit-learn (Isolation Forest)
* **Data Processing:** Pandas, NumPy
* **Visualization:** Streamlit
* **Deployment:** Docker
* **Alerts:** SMTP (Email)

---

## 🚀 Future Enhancements

* Real-time streaming (Kafka / Kinesis)
* Integration with AWS CloudWatch / API Gateway
* Automated IP blocking at firewall level
* Advanced models (LSTM / Deep Learning)
* Authentication & RBAC
* Alert dashboards with Grafana

---

## 👩‍💻 Author

**Kiranmayee Avula**
B.Tech CSE | AI & Cloud Enthusiast

---

## ⭐ Project Highlights

* End-to-end ML pipeline
* Real-time monitoring system
* Cloud-ready architecture
* Production-style implementation
* Strong DevOps + AI integration

---
