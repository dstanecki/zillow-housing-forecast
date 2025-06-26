# 🏡 Zillow Housing Forecast

A containerized Python Flask web application that predicts the estimated one-year percent change in home values for any given ZIP code in the U.S.

## ⚡ TL;DR: Quick Start
Helm Single-Node Deployment: 
```bash
helm install /home/daniel/zillow-housing-forecast/deployments/helm/zhf-chart-0.1.0.tgz --generate-name
```

Helm Multi-Node Deployment: 
```bash
helm install /home/daniel/zillow-housing-forecast/deployments/helm/zhf-chart-0.1.0.tgz --generate-name --set replicaCount=2 # Or more
```

Standard Deployment (keeping 2 replicas default for simplicity):
```bash
kubectl apply -f deployments/k8s/namespace.yaml
kubectl apply -f deployments/k8s/ -n zhf
```
---

## 🔍 About

This project uses historical Zillow data to forecast housing market trends. The data is smoothed and seasonally adjusted, meaning that it's been processed using a moving average to reduce short-term noise and seasonal effects. The app is built with Python and Flask, backed by a MariaDB database, and can be deployed in various environments using Docker Compose, Kubernetes, or AWS ECS Fargate.

## 🧱 Architecture

- **Frontend**: Multi-arch Python Flask app (linux/amd64 and linux/arm64 compatibility ensures that the container runs seamlessly on Raspberry Pi OS, GKE, EKS, etc.)
- **Backend**: MariaDB
- **Namespace**: `zhf`

## 📋 Prerequisites

- Kubernetes 1.24+
- kubectl configured
- (Optional) Helm for deploying Helm chart

## 🚀 Standard Kubernetes Deployment Instructions

### Step 1: Clone this repo
```bash
git clone https://github.com/dstanecki/zillow-housing-forecast.git
cd zillow-housing-forecast
```
### Step 2: Create the 'zhf' namespace
```bash
kubectl apply -f deployments/k8s/namespace.yaml
```
### Step 3: Deploy all manifests
```bash
kubectl apply -f deployments/k8s/ -n zhf
```
### Step 4: Access the app via NodePort service or LoadBalancer (if configured)
#### NodePort 
![Node Port Visual](./images/nodePortVisual.png)

Based on my example above, the link would be http://192.168.12.199:30836
