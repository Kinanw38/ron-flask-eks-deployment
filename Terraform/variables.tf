variable "aws_region" {
  default = "us-east-1"
}

variable "project_name" {
  default = "ron-eks-mission"
}

variable "vpc_cidr" {
  default = "10.0.0.0/16"
}

variable "instance_type" {
  default = "t3.small"
}

# מושך את רשימת ה-Availability Zones הזמינים באזור שלך
data "aws_availability_zones" "available" {
  state = "available"
}