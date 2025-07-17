# ArgoCD Configuration

This folder (`infra/argocd/`) contains all ArgoCD-related configuration and deployment manifests for managing the `zhf` application in both `dev` and `prod` environments using GitOps with Helm.

---

## 📁 Files Overview

| File | Purpose |
|------|---------|
| `argocd-ingress.yaml` | Exposes ArgoCD UI via Traefik using IngressRoute |
| `argocd-server-tls.yaml` | TLS secret or certificate definition for ArgoCD |
| `values.yaml` | Helm values file used to install or configure ArgoCD (e.g. `server.insecure: true`) |
| `zhf-dev.yaml` | ArgoCD `Application` resource for the **dev** environment (auto-sync enabled) |
| `zhf-prod.yaml` | ArgoCD `Application` resource for the **prod** environment (manual sync) |

---

## Install ArgoCD from Helm 
helm install argocd argo/argo-cd -n argocd --values values.yaml

## 🧠 Environments

### 🔁 Dev (`zhf-dev`)
- Auto-sync enabled (`syncPolicy.automated`)
- Tracks changes from `values-dev.yaml`
- Resources deployed into namespace: `dev`
- Suitable for fast iteration and testing

### 🔒 Prod (`zhf-prod`)
- Manual sync (no automation)
- Tracks `values-prod.yaml`
- Resources deployed into namespace: `prod`
- Intended for controlled, approved releases

---

## 🚀 Deployment Instructions

### 1. Apply Applications to ArgoCD

```bash
kubectl apply -f zhf-dev.yaml
kubectl apply -f zhf-prod.yaml
