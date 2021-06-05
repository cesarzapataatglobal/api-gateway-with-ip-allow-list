terraform {
  backend "s3" {
    bucket = "api-gateway-lambda-authorizer-state"
    key    = "terraform.tfstate"
    region = "us-east-1"
  }
}
