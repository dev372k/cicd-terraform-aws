variable "aws_region" {
  default = "us-east-1"
}

variable "project_name" {
  default = "fastapi"
}

variable "container_image" {
  description = "ECR image URL"
}