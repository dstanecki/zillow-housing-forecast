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
resource "kubernetes_secret" "db_password" {
  metadata {
    name      = "db-password"
    namespace = "dev"
  }

  string_data = {
    DB_PASSWORD = var.db_password
  }

  type = "Opaque"
}
resource "kubernetes_secret" "db_password" {
  metadata {
    name      = "db-password"
    namespace = "prod"
  }

  string_data = {
    DB_PASSWORD = var.db_password
  }

  type = "Opaque"
}
resource "kubernetes_secret" "redis_password" {
  metadata {
    name      = "redis-password"
    namespace = "dev"
  }

  string_data = {
    redis-password = var.redis_password
  }

  type = "Opaque"
}
resource "kubernetes_secret" "redis_password" {
  metadata {
    name      = "redis-password"
    namespace = "prod"
  }

  string_data = {
    redis-password = var.redis_password
  }

  type = "Opaque"
}
resource "kubernetes_secret" "azure_ai_openapi_key" {
  metadata {
    name      = "azure-ai-openapi-key"
    namespace = "prod"
  }

  string_data = {
    SUBSCRIPTION_KEY = var.azure_ai_openapi_key
  }

  type = "Opaque"
}
resource "kubernetes_secret" "azure_ai_openapi_key" {
  metadata {
    name      = "azure-ai-openapi-key"
    namespace = "dev"
  }

  string_data = {
    SUBSCRIPTION_KEY = var.azure_ai_openapi_key
  }

  type = "Opaque"
}
resource "kubernetes_secret" "recaptcha_secret_key_prod" {
  metadata {
    name      = "recaptcha-secret-key"
    namespace = "prod"
  }

  string_data = {
    RECAPTCHA_SECRET_KEY = var.recaptcha_secret_key_prod
  }

  type = "Opaque"
}
resource "kubernetes_secret" "recaptcha_secret_key_dev" {
  metadata {
    name      = "recaptcha-secret-key"
    namespace = "dev"
  }

  string_data = {
    RECAPTCHA_SECRET_KEY = var.recaptcha_secret_key_dev
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

