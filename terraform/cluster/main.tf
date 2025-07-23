provider "google" {
  project = var.project_id
  region  = var.region
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

  location                 = var.region
  
  remove_default_node_pool = true

  initial_node_count = 1

  enable_l4_ilb_subsetting = true

  network    = google_compute_network.zhf_network.id
  subnetwork = google_compute_subnetwork.zhf_subnetwork.id

  ip_allocation_policy {
    # stack_type                    = "IPV4_IPV6"
    services_secondary_range_name = google_compute_subnetwork.zhf_subnetwork.secondary_ip_range[0].range_name
    cluster_secondary_range_name  = google_compute_subnetwork.zhf_subnetwork.secondary_ip_range[1].range_name
  }

  deletion_protection = false
}

resource "google_container_node_pool" "zhf_node_pool" {
  name       = "default-node-pool"
  cluster    = google_container_cluster.zhf_cluster.name
  location   = var.region

  node_count = 1

  node_config {
    machine_type = "e2-medium"
    oauth_scopes = [
      "https://www.googleapis.com/auth/cloud-platform",
    ]
  }
}
