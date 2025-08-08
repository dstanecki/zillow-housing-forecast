# 🏡 Zillow Housing Forecast

An AI-powered, containerized Python Flask web application that predicts the estimated 1-year percent change in home values for any given ZIP code in the U.S.

## Live Demo

https://zhf.danielstanecki.com

---

## 📚 Table of Contents

- [Overview](#-overview)
- [Tech Stack & Architecture](#-tech-stack--architecture)
  - [Components](#-components)
- [Disaster Recovery](#disaster-recovery-automated-failover-to-google-kubernetes-engine)
- [Service Level Indicators](#service-level-indicators)
- [Required Kubernetes Secrets](#required-kubernetes-secrets)
- [Contributing](#contributing)
- [License](#license)

## 🔍 Overview

This project leverages [Zillow’s housing data](https://www.zillow.com/research/data/) to forecast local market trends at the ZIP code level. The data is **smoothed and seasonally adjusted** to reduce noise and emphasize long-term trends.

Beyond traditional forecasting, the app integrates **AI with live web search grounding** to explain the factors influencing each prediction.

This app runs in a self-hosted Kubernetes homelab (Raspberry Pi cluster) with automated failover to Google Kubernetes Engine (GKE) for disaster recovery.

| ![Front End](/images/frontend.png) |
|:--:| 
| *Front end* |

## 🧰 Tech Stack & Architecture

This application is fully containerized and designed for **scalability and high availability (HA)** across a **multi-node Kubernetes cluster**.

### 📦 Components

- **Frontend**: Python Flask web app (multi-arch Docker container)
- **Backend**: MariaDB
- **Highly Available Deployment**: Kubernetes + ArgoCD + Helm
- **AI Integration**: Azure OpenAI + Bing Web Search (real-time grounding for explanatory summaries)
- **Caching & L7 Rate Limiting**: Redis
- **Reverse Proxy**: Traefik (via Cloudflare Tunnel)
- **TLS Management**: cert-manager + Let’s Encrypt
- **Observability**: Prometheus + Grafana
- **CI/CD**: GitHub Actions pulls new Zillow dataset on the 17th of every month and rebuilds my db container image

| ![Architectural Diagram](/images/k8s-ingress-letsencrypt.drawio.png) |
|:--:| 
| *Network Architecture of Traefik Reverse Proxy + CloudFlare Tunnel + cert-manager* |

## Disaster Recovery: Automated Failover to Google Kubernetes Engine

This application has fully automated disaster recovery in case scheduled health checks fail. A GitHub Actions workflow pings an HTTP endpoint in the cluster’s app every 5 minutes and triggers the deploy-to-GKE pipeline after 3 consecutive failures. The GKE pipeline deploys the app to cloud in a zero-touch fashion and redirects the DNS record.

| ![disaster_recovery.drawio.png](/images/disaster_recovery.drawio.png) |
|:--:| 
| *Disaster recovery workflow from homelab to GKE* |

## Service Level Indicators

Uses [Upptime](https://upptime.js.org/) for external uptime monitoring. See live monitoring here (beginning from August 7th, 2025): https://www.danielstanecki.com/zhf-upptime/

| ![upptime.png](/images/upptime.png) |
|:--:| 
| *Service Level Indicator* |

Through disaster recovery and pre-deployment testing in staging, I aim to maintain **>99.99% uptime** for this app.

## Required Kubernetes Secrets

- db-password (password for mariadb user)
- azure-ai-openapi-key (from Azure AI Foundry portal)
- redis-password (redis password, create this manually instead of using the default generated one. Avoids password regeneration if you ever reinstall redis)
- recaptcha-secret-key (created when you add your domain to Google reCAPTCHA)
- tunnel-token (passed to cloudflared agent deployment)

## Contributing

This project depends on a number of external services (AzureAI, Redis, Cloudflare, ReCAPTCHA, etc.), so local deployment requires some manual configuration.

## License

This project is licensed under the MIT License – see the [LICENSE](./LICENSE) file for details.
