terraform {
  required_version = ">= 1.0"

  backend "gcs" {
    bucket  = "zhf-tfstate-bucket"
    prefix  = "terraform/state"
  }
}
