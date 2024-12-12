terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 5.80.0"
    }
  }
  backend "s3" {
    bucket = "fiap-tech-challenge-terraform"
    key    = "fiap-tech-challenge-terraform-ecr/terraform.tfstate"
    region = "us-east-1"
  }
}

provider "aws" {
  region = "us-east-1"
}
