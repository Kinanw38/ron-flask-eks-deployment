output "cluster_name" {
  description = "The name of the EKS cluster"
  value       = aws_eks_cluster.main.name
}

output "cluster_endpoint" {
  description = "The endpoint for your EKS cluster API"
  value       = aws_eks_cluster.main.endpoint
}

output "ecr_repository_url" {
  description = "The URL of the ECR repository"
  value       = aws_ecr_repository.repo.repository_url
}

output "region" {
  value = var.aws_region
}

output "cluster_iam_role_arn" {
  description = "IAM role ARN used by the EKS cluster control plane"
  value       = aws_iam_role.cluster.arn
}

output "node_iam_role_arn" {
  description = "IAM role ARN used by the EKS worker nodes"
  value       = aws_iam_role.nodes.arn
}

output "vpc_id" {
  description = "VPC ID"
  value       = aws_vpc.main.id
}