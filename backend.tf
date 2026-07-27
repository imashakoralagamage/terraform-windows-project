terraform {

  backend "s3" {
    bucket = "terraform-state-imasha"
    key    = "windows-server/terraform.tfstate"
    region = "ap-southeast-1"
  }

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}