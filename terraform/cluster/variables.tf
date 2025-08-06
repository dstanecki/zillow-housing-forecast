variable "project_id" {
  description = "The GCP project ID"
  type        = string
}

variable "region" {
  description = "The GCP region to deploy to"
  type        = string
  default     = "us-east4"
}

variable "zone" {
  description = "The GCP zone to deploy the cluster in"
  default     = "us-east4-a"
}

variable "cluster_name" {
  description = "The name of the GKE Autopilot cluster"
  type        = string
  default     = "zhf-cluster"
}
