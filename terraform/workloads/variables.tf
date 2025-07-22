variable "project_id" {
  type = string
}

variable "region" {
  type    = string
  default = "us-central1"
}

variable "terraform_service_account_email" {
  type = string
  default = "zhf-terraform@zhf-project-1752025280949.iam.gserviceaccount.com"
}
