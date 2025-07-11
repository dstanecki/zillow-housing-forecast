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
- **Highly Available Deployment**: Kubernetes + Helm
- **AI Integration**: Azure OpenAI + Bing Web Search (real-time grounding for explanatory summaries)
- **Caching & L7 Rate Limiting**: Redis
- **Reverse Proxy**: Traefik (via Cloudflare Tunnel)
- **TLS Management**: cert-manager + Let’s Encrypt
- **Observability**: Prometheus + Grafana
- **CI/CD**: GitHub Actions pulls new Zillow dataset on the 17th of every month and rebuilds my db container image


| ![Architectural Diagram](/images/k8s-ingress-letsencrypt.drawio.png) |
|:--:| 
| *Network Architecture of Traefik Reverse Proxy + CloudFlare Tunnel + cert-manager* |

### Kubernetes Secrets

To run this app, several secrets are passed as env variables:

- db-password (password for mariadb user)
- azure-ai-openapi-key (from Azure AI Foundry portal)
- my-redis (redis password that's auto-generated with the Redis Helm install)
- recaptcha-secret-key (created when you add your domain to Google reCAPTCHA)
- tunnel-token (passed to cloudflared agent deployment)

### Other Helm Charts Required

| NAME         | NAMESPACE   | CHART                           | APP VERSION |
|--------------|-------------|----------------------------------|-------------|
| my-redis     | prod        | redis-21.2.6                     | 8.0.2       |
| prometheus   | monitoring  | kube-prometheus-stack-75.7.0     | v0.83.0     |
| traefik      | kube-system | traefik-27.0.201+up27.0.2        | v2.11.10    |
| traefik-crd  | kube-system | traefik-crd-27.0.201+up27.0.2    | v2.11.10    |

## Contributing

Due to the need for an individual AzureAI API Key, a recaptcha secret key, CloudFlare tunnel configuration, and external Helm charts, deploying on your local machine would require lengthy configuration.

## License

This project is licensed under the MIT License – see the [LICENSE](./LICENSE) file for details.
