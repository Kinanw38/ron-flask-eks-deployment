terraform {
  required_version = ">= 1.0"

  backend "s3" {
    # Bucket name is passed at init time (local: -backend-config or CI: TF_STATE_BUCKET secret)
    key     = "eks/terraform.tfstate"
    region  = "us-east-1"
    encrypt = true
  }

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}