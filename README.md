# 🚀 Cloud API Attack Detection System

## 🔐 Overview

This project is a **real-time API security system** that monitors API traffic, analyzes behavior patterns, and detects suspicious activity using machine learning.

The system automatically generates alerts, sends email notifications, and simulates blocking of malicious IPs — enabling **intelligent, behavior-based threat detection** instead of static rules.

---

## 🎯 Problem Statement

Modern applications face continuous API abuse such as:

* Brute-force login attempts
* Abnormal request spikes
* Unauthorized endpoint access
* Data scraping and bot traffic

Traditional rule-based systems fail to detect evolving attack patterns.

👉 This project solves that using **machine learning-based anomaly detection**.

---

## ⚙️ System Architecture

```
User Request
     ↓
FastAPI Middleware
     ↓
Request Logging (CSV)
     ↓
Feature Engineering
     ↓
ML Model (Isolation Forest)
     ↓
Prediction (Normal / Suspicious)
     ↓
Alert Engine
     ↓
Email Notification + Block Simulation
     ↓
Dashboard Visualization
```

---

## 🧠 Key Features

* ✅ Real-time API request monitoring
* ✅ Behavior-based anomaly detection (Isolation Forest)
* ✅ Automatic alert generation
* ✅ Email notifications for suspicious activity
* ✅ Simulated IP blocking mechanism
* ✅ REST API endpoints for logs, predictions, alerts
* ✅ Modular pipeline (easy to extend)
* ✅ Docker-ready architecture

---

## 🛠️ Tech Stack

* **Backend:** FastAPI
* **Machine Learning:** Scikit-learn (Isolation Forest)
* **Data Processing:** Pandas, NumPy
* **Visualization:** Streamlit
* **Alerting:** SMTP (Email)
* **Containerization:** Docker

---

## 📂 Project Structure

```
cloud-api-attack-detection/
│
├── api/
│   ├── server.py
│   ├── alerting.py
│
├── ml/
│   ├── realtime_features.py
│   ├── realtime_predict.py
│   ├── alert_engine.py
│
├── data/
│
├── model/
│   └── api_attack_model.pkl
│
├── dashboard/
│   └── app.py
│
├── requirements.txt
├── Dockerfile
└── README.md
```

---

## 🚀 How to Run

### 1️⃣ Clone repository

```bash
git clone https://github.com/Kiranmayee714/cloud-api-attack-detection.git
cd cloud-api-attack-detection
```

---

### 2️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

---

### 3️⃣ Setup environment variables

Create `.env` file:

```env
EMAIL_SENDER=your_email@gmail.com
EMAIL_PASSWORD=your_app_password
EMAIL_RECEIVER=your_email@gmail.com
```

---

### 4️⃣ Run the API

```bash
uvicorn api.server:app --reload
```

Open:

```
http://127.0.0.1:8000/docs
```

---

### 5️⃣ Generate traffic

```
http://127.0.0.1:8000/login
http://127.0.0.1:8000/admin
http://127.0.0.1:8000/data
```

---

### 6️⃣ View outputs

```
/logs
/predictions
/alerts
/blocked-ips
```

---

## 📊 Machine Learning Approach

* Model: **Isolation Forest**
* Detects anomalies based on:

  * Request frequency
  * Failed requests
  * Unique endpoints accessed
  * Payload size
  * Behavioral patterns

👉 Instead of predefined rules, the system learns **normal behavior** and flags deviations.

---

## 🔔 Alert System

When suspicious activity is detected:

* Alert is logged
* Email is sent to admin
* IP is added to blocked list

---

## ⚡ Performance Optimization

* Non-blocking API design using background threads
* Fast response time with asynchronous processing
* ML pipeline runs independently from request handling

---



## 🧪 Demo Flow

1. Hit API endpoints repeatedly
2. System logs behavior
3. ML detects anomaly
4. Alert is generated
5. Email notification sent
6. IP marked as suspicious

---

