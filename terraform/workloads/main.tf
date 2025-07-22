provider "google" {
  project = var.project_id
  region  = var.region
}

data "google_client_config" "default" {}

data "terraform_remote_state" "cluster" {
  backend = "gcs"
  config = {
    bucket = "zhf-tfstate-bucket"
    prefix = "terraform/state"
  }
}

locals {
  k8s_connection = {
    host                   = data.terraform_remote_state.cluster.outputs.cluster_endpoint
    token                  = data.google_client_config.default.access_token
    cluster_ca_certificate = base64decode(data.terraform_remote_state.cluster.outputs.ca_certificate)
  }
}

provider "kubernetes" {
  host                   = local.k8s_connection.host
  token                  = local.k8s_connection.token
  cluster_ca_certificate = local.k8s_connection.cluster_ca_certificate
}

provider "helm" {
  kubernetes = local.k8s_connection
}

# Give GCP service account k8s privilege
resource "kubernetes_cluster_role_binding" "terraform_cluster_admin" {
  metadata {
    name = "terraform-cluster-admin"
  }

  role_ref {
    api_group = "rbac.authorization.k8s.io"
    kind      = "ClusterRole"
    name      = "cluster-admin"
  }

  subject {
    kind      = "User"
    name      = var.terraform_service_account_email
    api_group = "rbac.authorization.k8s.io"
  }
}

# Install ArgoCD
resource "helm_release" "argocd" {
  name       = "argocd"
  namespace  = "argocd"
  repository = "https://argoproj.github.io/argo-helm"
  chart      = "argo-cd"
  version    = "8.1.3" # check latest: https://artifacthub.io/packages/helm/argo/argo-cd
  create_namespace = true
  values = [file("../argo/apps/argocd/values.yaml")]
}
