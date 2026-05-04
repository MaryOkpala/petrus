terraform {
  required_version = ">= 1.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
  backend "s3" {
    bucket         = "petrus-terraform-state-007448416489"
    key            = "environments/web-app/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "petrus-terraform-locks"
    encrypt        = true
  }
}

provider "aws" {
  region = var.aws_region
  default_tags {
    tags = {
      Project     = "Petrus"
      Type        = "web-app"
      Team        = var.team
      Environment = var.environment
      ManagedBy   = "Petrus"
      CostCenter  = var.team
    }
  }
}

module "networking" {
  source              = "../../modules/networking"
  project             = "petrus"
  team                = var.team
  environment         = var.environment
  vpc_cidr            = var.vpc_cidr
  public_subnet_cidr  = var.public_subnet_cidr
  private_subnet_cidr = var.private_subnet_cidr
  availability_zone   = var.availability_zone
}

module "security" {
  source      = "../../modules/security"
  project     = "petrus"
  team        = var.team
  environment = var.environment
  vpc_id      = module.networking.vpc_id
  vpc_cidr    = module.networking.vpc_cidr
}
