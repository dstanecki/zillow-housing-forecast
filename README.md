# 🏡 Zillow Housing Forecast

An AI-powered, containerized Python Flask web application that predicts the estimated 1-year percent change in home values for any given ZIP code in the U.S.

## Live Demo Link
https://zhf.danielstanecki.com


| ![Front End](/images/frontend.png) |
|:--:| 
| *Front end* |

## 🔍 Overview

This project leverages **Zillow’s housing data** to forecast local market trends at the ZIP code level. The data is **smoothed and seasonally adjusted** to reduce noise and emphasize long-term trends.

Beyond traditional forecasting, the app integrates **AI with live web search grounding** to explain the factors influencing each prediction.

---

## 🧰 Tech Stack & Architecture

This application is fully containerized and designed for **scalability and high availability (HA)** across a **multi-node Kubernetes cluster**.

### 📦 Components

- **Frontend**: Python Flask web app (multi-arch Docker container)
- **Backend**: MariaDB (stateless, horizontally scalable with optional replication)
- **Highly Available Deployment**: Kubernetes + Helm
- **AI Integration**: Azure OpenAI + Bing Web Search (real-time grounding for explanatory summaries)
- **Caching & L7 Rate Limiting**: Redis
- **Reverse Proxy**: Traefik (via Cloudflare Tunnel)
- **TLS Management**: cert-manager + Let’s Encrypt
- **Observability**: Prometheus + Grafana


| ![Architectural Diagram](/images/k8s-ingress-letsencrypt.drawio.png) |
|:--:| 
| *Network Architecture of Traefik Reverse Proxy + CloudFlare Tunnel + cert-manager* |