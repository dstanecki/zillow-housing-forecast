provider "google" {
  project = var.project_id
  region  = var.region
}

data "google_client_config" "default" {}

data "terraform_remote_state" "cluster" {
  backend = "gcs"
  config = {
    bucket = "zhf-tfstate-bucket"
    prefix = "terraform/cluster"
  }
}

locals {
  k8s_connection = {
    host                   = "https://${data.terraform_remote_state.cluster.outputs.cluster_endpoint}"
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

# SECRETS
resource "kubernetes_secret" "db_password_dev" {
  metadata {
    name      = "db-password"
    namespace = "dev"
  }

  data = {
    DB_PASSWORD = var.db_password
  }

  type = "Opaque"
}
resource "kubernetes_secret" "db_password_prod" {
  metadata {
    name      = "db-password"
    namespace = "prod"
  }

  data = {
    DB_PASSWORD = var.db_password
  }

  type = "Opaque"
}
resource "kubernetes_secret" "redis_password_dev" {
  metadata {
    name      = "redis-password"
    namespace = "dev"
  }

  data = {
    redis-password = var.redis_password
  }

  type = "Opaque"
}
resource "kubernetes_secret" "redis_password_prod" {
  metadata {
    name      = "redis-password"
    namespace = "prod"
  }

  data = {
    redis-password = var.redis_password
  }

  type = "Opaque"
}
resource "kubernetes_secret" "azure_ai_openapi_key_prod" {
  metadata {
    name      = "azure-ai-openapi-key"
    namespace = "prod"
  }

  data = {
    SUBSCRIPTION_KEY = var.azure_ai_openapi_key
  }

  type = "Opaque"
}
resource "kubernetes_secret" "azure_ai_openapi_key_dev" {
  metadata {
    name      = "azure-ai-openapi-key"
    namespace = "dev"
  }

  data = {
    SUBSCRIPTION_KEY = var.azure_ai_openapi_key
  }

  type = "Opaque"
}
resource "kubernetes_secret" "recaptcha_secret_key_prod" {
  metadata {
    name      = "recaptcha-secret-key"
    namespace = "prod"
  }

  data = {
    RECAPTCHA_SECRET_KEY = var.recaptcha_secret_key_prod
  }

  type = "Opaque"
}
resource "kubernetes_secret" "recaptcha_secret_key_dev" {
  metadata {
    name      = "recaptcha-secret-key"
    namespace = "dev"
  }

  data = {
    RECAPTCHA_SECRET_KEY = var.recaptcha_secret_key_dev
  }

  type = "Opaque"
}
resource "kubernetes_secret" "cloudflare_api_token_secret" {
  metadata {
    name      = "cloudflare-api-token-secret"
    namespace = "cert-manager"
  }

  data = {
    api-token = var.cloudflare_api_token_secret
  }

  type = "Opaque"
}

# Install app of apps
resource "kubernetes_manifest" "app_of_apps" {
  manifest = {
    apiVersion = "argoproj.io/v1alpha1"
    kind       = "Application"
    metadata = {
      name      = "app-of-apps"
      namespace = "argocd"
    }
    spec = {
      project = "default"
      source = {
        repoURL        = "https://github.com/dstanecki/zillow-housing-forecast.git"
        targetRevision = "HEAD"
        path           = "argo/apps"
        directory = {
          recurse = true
        }
      }
      destination = {
        server    = "https://kubernetes.default.svc"
        namespace = "argocd"
      }
      syncPolicy = {
        automated = {
          prune    = true
          selfHeal = true
        }
      }
    }
  }
}

