# Terraform to provision app on GKE

## Cluster 

- Bootstraps the cluster infrastructure components
- Some helm packages and CRDs are installed here as they are prerequisites for the workloads provisioning

## Workloads

- Provisions cluster admin role binding for GCP service account
- Creates kubernetes secret objects
- Installs ArgoCD "App of Apps"
