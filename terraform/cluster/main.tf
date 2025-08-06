provider "google" {
  project = var.project_id
  region  = var.region
}

provider "helm" {
  kubernetes = {
    host                   = "https://${google_container_cluster.zhf_cluster.endpoint}"
    token                  = data.google_client_config.default.access_token
    cluster_ca_certificate = base64decode(google_container_cluster.zhf_cluster.master_auth[0].cluster_ca_certificate)
  }
}

provider "kubernetes" {
  host                   = "https://${google_container_cluster.zhf_cluster.endpoint}"
  token                  = data.google_client_config.default.access_token
  cluster_ca_certificate = base64decode(google_container_cluster.zhf_cluster.master_auth[0].cluster_ca_certificate)
}

data "google_client_config" "default" {}

resource "google_compute_network" "zhf_network" {
  name = "zhf-network"

  auto_create_subnetworks  = false
  enable_ula_internal_ipv6 = true
}

resource "google_compute_subnetwork" "zhf_subnetwork" {
  name = "zhf-subnetwork"

  ip_cidr_range = "10.0.0.0/16"
  region        = var.region

  stack_type       = "IPV4_IPV6"
  ipv6_access_type = "INTERNAL" # Change to "EXTERNAL" if creating an external loadbalancer

  network = google_compute_network.zhf_network.id
  
  secondary_ip_range {
    range_name    = "services-range"
    ip_cidr_range = "192.168.16.0/24"
  }

  secondary_ip_range {
    range_name    = "pod-ranges"
    ip_cidr_range = "192.168.0.0/20"
  }
}

resource "google_container_cluster" "zhf_cluster" {
  name = var.cluster_name

  location                 = var.zone # SINGLE ZONE DEPLOYMENT
  
  remove_default_node_pool = true

  initial_node_count = 2

  enable_l4_ilb_subsetting = true

  network    = google_compute_network.zhf_network.id
  subnetwork = google_compute_subnetwork.zhf_subnetwork.id

  ip_allocation_policy {
    # stack_type                    = "IPV4_IPV6"
    services_secondary_range_name = google_compute_subnetwork.zhf_subnetwork.secondary_ip_range[0].range_name
    cluster_secondary_range_name  = google_compute_subnetwork.zhf_subnetwork.secondary_ip_range[1].range_name
  }

  deletion_protection = false

  timeouts {
    create = "20m"
    update = "20m"
    delete = "15m"
  }
}

resource "google_container_node_pool" "zhf_node_pool" {
  name       = "zhf-node-pool"
  cluster    = google_container_cluster.zhf_cluster.name
  location   = var.zone

  autoscaling {
    min_node_count = 2
    max_node_count = 3
  }

  node_config {
    machine_type = "e2-standard-2"
    oauth_scopes = [
      "https://www.googleapis.com/auth/cloud-platform",
    ]
  }

  management {
    auto_repair  = true
    auto_upgrade = true
  }

  upgrade_settings {
    max_surge       = 1
    max_unavailable = 0
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
  values = [file("../../argo/apps/argocd/values.yaml")]

  timeout    = 900
  force_update = true

  lifecycle {
    prevent_destroy = false
  }
}

resource "helm_release" "cert_manager" {
  name       = "cert-manager"
  namespace  = "cert-manager"
  repository = "https://charts.jetstack.io"
  chart      = "cert-manager"
  version    = "v1.18.0"
  create_namespace = true
  values = [file("../../argo/apps/cert-manager/values.yaml")]
}

resource "helm_release" "kube_prometheus_stack" {
  name       = "kube-prometheus-stack"
  namespace  = "monitoring"
  repository = "https://prometheus-community.github.io/helm-charts"
  chart      = "kube-prometheus-stack"
  version    = "75.11.0" 

  create_namespace = true
}

resource "helm_release" "traefik" {
  name       = "traefik"
  namespace  = "kube-system"
  repository = "https://helm.traefik.io/traefik"
  chart      = "traefik"
  version    = "36.3.0" 

  create_namespace = true
}

data "kubernetes_service" "traefik" {
  metadata {
    name      = "traefik"
    namespace = "kube-system"
  }

  depends_on = [helm_release.traefik]
}

resource "kubernetes_namespace" "dev" {
  metadata {
    name = "dev"
  }
}

resource "kubernetes_namespace" "prod" {
  metadata {
    name = "prod"
  }
}
