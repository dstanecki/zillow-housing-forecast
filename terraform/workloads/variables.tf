variable "project_id" {
  type = string
}

variable "region" {
  type    = string
  default = "us-east4"
}

variable "terraform_service_account_email" {
  type = string
  default = "zhf-terraform@zhf-project-1752025280949.iam.gserviceaccount.com"
}

variable "db_password" {
  type      = string
  sensitive = true
}

variable "redis_password" {
  type      = string
  sensitive = true
}

variable "azure_ai_openapi_key" {
  type      = string
  sensitive = true
}

variable "recaptcha_secret_key_dev" {
  type      = string
  sensitive = true
}

variable "recaptcha_secret_key_prod" {
  type      = string
  sensitive = true
}

variable "cloudflare_api_token_secret" {
  type      = string
  sensitive = true
}
