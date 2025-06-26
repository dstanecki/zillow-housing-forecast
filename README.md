# 🏡 Zillow Housing Forecast

A containerized Python Flask web application that predicts the estimated one-year percent change in home values for any given ZIP code in the U.S.

## ⚡ TL;DR: Quick Start
Helm Single-Node Deployment: 
```bash
helm install zhf ./deployments/helm/zhf-chart-0.1.0.tgz
```

Helm Multi-Node Deployment (2 replicas or more): 
```bash
helm install zhf ./deployments/helm/zhf-chart-0.1.0.tgz --set replicaCount=2
```

## 🔍 About

This project uses historical Zillow data to forecast housing market trends. The data is smoothed and seasonally adjusted, meaning that it's been processed using a moving average to reduce short-term noise and seasonal effects. The app is built with Python and Flask, backed by a MariaDB database, and can be deployed in various environments using Docker Compose, Kubernetes, or AWS ECS Fargate.

## 🧱 Architecture

- **Frontend**: Multi-arch Python Flask app (linux/amd64 and linux/arm64 compatibility ensures that the container runs seamlessly on Raspberry Pi OS, GKE, EKS, etc.)
- **Backend**: MariaDB (fully stateless, replicated if desired)
- **Namespace**: `zhf`

## 📋 Prerequisites

- Kubernetes v1.24+
- kubectl configured
- Helm v3.18.3+

## 🚀 Helm Deployment Instructions

### Step 1: Clone this repo
```bash
git clone https://github.com/dstanecki/zillow-housing-forecast.git
cd zillow-housing-forecast
```
### Step 2: Install Helm chart
- By default, the application is deployed with a single replica for both app and db deployments. You can increase this using `--set replicaCount=N` for horizontal scaling 
- If replicaCount > 1, then a soft anti-affinity rule is applied to distribute the pods evenly across nodes
```bash
helm install zhf ./deployments/helm/zhf-chart-0.1.0.tgz
```

### Step 3: Access the app via NodePort service
```bash
kubectl get svc # Retrieve the app svc NodePort
```
![Node Port Visual](./images/nodePortVisual.png)

Based on my example above, the link would be http://192.168.12.199:30836

### Step 4: Uninstall (Optional)
```bash 
helm uninstall zhf
```
