output "project_id" {
  description = "The GCP project ID"
  value       = var.project_id
}

output "region" {
  description = "Region where the GKE cluster is deployed"
  value       = var.region
}

output "cluster_name" {
  description = "Name of the GKE cluster"
  value       = google_container_cluster.zhf_cluster.name
}

output "cluster_endpoint" {
  description = "The endpoint of the GKE cluster"
  value       = google_container_cluster.zhf_cluster.endpoint
}

output "network_name" {
  description = "The name of the VPC network"
  value       = google_compute_network.zhf_network.name
}

output "subnetwork_name" {
  description = "The name of the subnetwork"
  value       = google_compute_subnetwork.zhf_subnetwork.name
}

output "gke_auth_command" {
  description = "Command to configure kubectl for this GKE cluster"
  value       = "gcloud container clusters get-credentials ${google_container_cluster.zhf_cluster.name} --region ${var.region} --project ${var.project_id}"
}

output "ca_certificate" {
  description = "Cluster CA certificate (base64)"
  value       = google_container_cluster.zhf_cluster.master_auth[0].cluster_ca_certificate
}
