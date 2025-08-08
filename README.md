# 🏡 Zillow Housing Forecast

An AI-powered, containerized Python Flask web application that predicts the estimated 1-year percent change in home values for any given ZIP code in the U.S.

## Live Demo Link
https://zhf.danielstanecki.com


| ![Front End](/images/frontend.png) |
|:--:| 
| *Front end* |

## 🔍 Overview

This project leverages [Zillow’s housing data](https://www.zillow.com/research/data/) to forecast local market trends at the ZIP code level. The data is **smoothed and seasonally adjusted** to reduce noise and emphasize long-term trends.

Beyond traditional forecasting, the app integrates **AI with live web search grounding** to explain the factors influencing each prediction.

---

## 🧰 Tech Stack & Architecture

This application is fully containerized and designed for **scalability and high availability (HA)** across a **multi-node Kubernetes cluster**.

### 📦 Components

- **Frontend**: Python Flask web app (multi-arch Docker container)
- **Backend**: MariaDB (stateless, horizontally scalable with optional replication)
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

This application has fully automated disaster recovery in case scheduled health checks fail. 

| ![disaster_recovery.drawio.png](/images/disaster_recovery.drawio.png) |
|:--:| 
| *Disaster recovery workflow from homelab to GKE* |

## Service Level Indicator Monitoring

Uses [Upptime](https://upptime.js.org/) for external uptime monitoring. See live monitoring here (beginning from August 7th, 2025): https://www.danielstanecki.com/zhf-upptime/

| ![upptime.png](/images/upptime.png) |
|:--:| 
| *Service Level Indicator* |

Through my disaster recovery solutions and by testing changes in my staging env first, I hope to keep my uptime above 99.99%.

### Kubernetes Secrets

- db-password (password for mariadb user)
- azure-ai-openapi-key (from Azure AI Foundry portal)
- redis-password (redis password, create this manually instead of using the default generated one. Avoids password regeneration if you ever reinstall redis)
- recaptcha-secret-key (created when you add your domain to Google reCAPTCHA)
- tunnel-token (passed to cloudflared agent deployment)

## Contributing

Due to the need for an individual AzureAI API Key, a recaptcha secret key, CloudFlare tunnel configuration, and external Helm charts, deploying on your local machine would require lengthy configuration.

## License

This project is licensed under the MIT License – see the [LICENSE](./LICENSE) file for details.
