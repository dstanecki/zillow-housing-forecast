# 🏡 Zillow Housing Forecast

A containerized Python Flask web application that predicts the estimated one-year percent change in home values for any given ZIP code in the U.S.

## ⚡ TL;DR: Quick Start
```bash
kubectl apply -f deployments/kubernetes/namespace.yaml
kubectl apply -f deployments/kubernetes/ -n zhf
```
---

## 🔍 About

This project uses historical Zillow data to forecast housing market trends. The data is smoothed and seasonally adjusted, meaning that it's been processed using a moving average to reduce short-term noise and seasonal effects. The app is built with Python and Flask, backed by a MariaDB database, and can be deployed in various environments using Docker Compose, Kubernetes, or AWS ECS Fargate.

## 🧱 Architecture

- **Frontend**: Multi-arch Python Flask app (linux/amd64 and linux/arm64 compatibility ensures that the container runs seamlessly on Raspberry Pi OS, GKE, EKS, etc.)
- **Backend**: MariaDB with PersistentVolume. The database is automatically initialized and populated by dbcreation-script.yaml which is mounted as a ConfigMap
- **Namespace**: `zhf`
- **Storage**: Local PVC

## 📋 Prerequisites

- Kubernetes 1.24+
- kubectl configured
- (Optional) K3s / Minikube / Kind / GKE / EKS
- (Optional) MetalLB installed (if using `LoadBalancer` in local cluster)

## 🚀 Kubernetes Deployment Instructions

### Step 1: Clone this repo
```bash
git clone https://github.com/dstanecki/zillow-housing-forecast.git
cd zillow-housing-forecast
```
### Step 2: Create the 'zhf' namespace
```bash
kubectl apply -f deployments/kubernetes/namespace.yaml
```
### Step 3: Deploy all manifests
```bash
kubectl apply -f deployments/kubernetes/ -n zhf
```
### Step 4: Access the app via NodePort service or LoadBalancer (if configured)
#### NodePort 
![Node Port Visual](./images/nodePortVisual.png)

Based on my example above, the link would be http://192.168.12.199:30836
