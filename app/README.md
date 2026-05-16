# Flask App — Build & Push to ECR

## Prerequisites

- Docker installed
- AWS CLI configured (`aws configure`)
- ECR repository already created (`terraform apply` in `../Terraform`)

## Build

From this directory (`app/`):

```bash
docker build -t flask-app:latest .
```

## Push to ECR

Replace placeholders with values from `terraform output` in the Terraform directory.

```bash
# Login to ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com

# Tag and push
docker tag flask-app:latest <ECR_REPOSITORY_URL>:latest
docker push <ECR_REPOSITORY_URL>:latest
```

Example if `ecr_repository_url` is `123456789.dkr.ecr.us-east-1.amazonaws.com/ron-eks-mission-repo`:

```bash
docker tag flask-app:latest 123456789.dkr.ecr.us-east-1.amazonaws.com/ron-eks-mission-repo:latest
docker push 123456789.dkr.ecr.us-east-1.amazonaws.com/ron-eks-mission-repo:latest
```
