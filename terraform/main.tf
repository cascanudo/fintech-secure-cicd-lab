provider "google" {
  project = "demo-project"
  region  = "us-central1"
}

resource "google_storage_bucket" "fintech_logs" {
  name     = "fintech-secure-lab-logs-demo"
  location = "US"

  uniform_bucket_level_access = false
}
