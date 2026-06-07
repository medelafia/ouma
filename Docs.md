# 📊 Ouma Tool – Kubernetes Deployment Documentation

This document describes how to deploy and configure the **Monitoring & Prediction System** on a Kubernetes cluster using the provided automation script and environment configuration files.

The system includes:
- Metrics collection (InfluxDB 2)
- Data storage (MySQL)
- Prediction service (AI/ML backend)
- Alerting system (Email + Slack)
- Kubernetes-based microservices architecture

---

# 🚀 1. Prerequisites

Before deployment, ensure you have:

- A running Kubernetes cluster (e.g., Oracle OKE, Minikube, or K8s cluster)
- `kubectl` configured and connected to your cluster
- Bash shell access
- Helm installed (if used in your cluster setup)
- Proper namespace created (if required by your setup)

---

# 📁 2. Project Deployment Structure

The deployment is fully automated using:

```bash
setup_all.sh
````

This script handles:

* Creating Kubernetes resources
* Deploying services and pods
* Injecting environment variables
* Setting up database and monitoring stack

---

# ⚙️ 3. Environment Configuration

The system requires **three `.env` files** before running deployment:

---

## 📌 3.1 `.env` (Main Application Config)

This file contains the core configuration for the monitoring and prediction system.

```env
INFLUX_DB_BUCKET=metrics
INFLUX_DB_ORG=ouma-org
INFLUX_DB_TOKEN=MyInitialAdminToken0==

MYSQL_USER=mysql_user
MYSQL_PASSWORD=mysql_user_password
MYSQL_DB=ouma

SECRET_KEY=secret_key

TARGET_SERVER_PORT=9090
TARGET_SERVER_HOST=prometheus-kube-prometheus-prometheus

PREDICTION_INTERVAL=3

ACTIVATE_EMAIL_ALERTING=True 
ACTIVATE_SLACK_ALERTING=True

SYSTEM_EMAIL=email@example.com
SMTP_SERVER=smtp.example.com
SMTP_PORT=587
SYSTEM_EMAIL_PASSWORD=app_password_mails

SLACK_TOKEN=slack_token
SLACK_CHANNEL=ouma-alerts
SLACK_USER=ouma-alerts-manager

INFLUX_DB_URL=http://influxdb-influxdb2:8086
```

---

## 📌 3.2 `.env.mysql` (MySQL Configuration)

Used for initializing and securing the MySQL database.

```env
MYSQL_ROOT_PASSWORD=password_root
MYSQL_DATABASE=ouma
MYSQL_USER=mysql_user
MYSQL_PASSWORD=mysql_user_password

mysql-root-password=password_root
mysql-database=ouma
mysql-username=mysql_user
mysql-password=mysql_user_password
```

---

## 📌 3.3 `.env.influxdb2` (InfluxDB Configuration)

Used for initializing InfluxDB 2 instance.

```env
admin-password=Password
admin-token=MyInitialAdminToken0==
```

---

# ⚡ 4. Deployment Steps

## 4.1 Configure environment files

Create the required files:

```bash
.env
.env.mysql
.env.influxdb2
```

Fill them with the values provided above.

---

## 4.2 Make deployment script executable

```bash
chmod +x setup_all.sh
```

---

## 4.3 Run deployment

```bash
./setup_all.sh
```

This will:

* Deploy MySQL
* Deploy InfluxDB 2
* Deploy monitoring services
* Deploy prediction backend
* Configure secrets & environment variables

---

# 📡 5. System Architecture Overview

The system is composed of the following components:

### 🗄️ Databases

* **MySQL** → stores structured application data
* **InfluxDB 2** → stores time-series metrics

### 📊 Monitoring Layer

* Collects system and application metrics
* Sends data to InfluxDB

### 🤖 Prediction Service

* Uses ML model to predict CPU/Memory usage
* Runs at interval defined by:

  ```
  PREDICTION_INTERVAL=3
  ```

### 🚨 Alerting System

* Email notifications via SMTP
* Slack notifications via Slack API

---

# 🔔 6. Alerting Configuration

## Email Alerts

Enable via:

```env
ACTIVATE_EMAIL_ALERTING=True
```

SMTP settings required:

* SMTP server
* Port
* System email credentials

## Slack Alerts

Enable via:

```env
ACTIVATE_SLACK_ALERTING=True
```

Required:

* Slack token
* Slack channel
* Slack bot user

---

# 🧪 7. Verification After Deployment

After deployment, verify services:

```bash
kubectl get pods -n monitoring
kubectl get services -n monitoring
kubectl get all -n monitoring
```

Check logs:

```bash
kubectl logs <pod-name> -n monitoring
```

---

# 🌐 8. Access Services

Depending on your Kubernetes setup:

* Prediction API → `http://<service-ip>:9090`
* InfluxDB UI → exposed via service or port-forward
* MySQL → internal cluster access only

---

# 🛠️ 9. Troubleshooting

### ❌ Pods not starting

Check:

```bash
kubectl describe pod <pod-name> -n monitoring
```

### ❌ Database connection issues

Ensure:

* Correct `.env.mysql` values
* MySQL service is running

### ❌ InfluxDB authentication error

Verify:

* `admin-token`
* `INFLUX_DB_TOKEN`

### ❌ Alerts not working

Check:

* SMTP credentials
* Slack token validity

---

# 📌 10. Security Recommendations

* Do NOT commit `.env` files to GitHub
* Use Kubernetes Secrets instead of plain environment files in production
* Rotate tokens regularly
* Restrict database access to cluster internal network

---

# 📈 11. Future Improvements

* Add Helm chart support
* Integrate Grafana dashboards
* Add autoscaling (HPA)
* Improve anomaly detection model
* Add centralized logging (ELK stack)

---

# 👨‍💻 Author

Monitoring System developed as part of a cloud-native infrastructure project using:

* Kubernetes
* Docker
* InfluxDB 2
* MySQL
* Python ML services
* Slack & Email alerting

---
