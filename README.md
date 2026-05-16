# 🚀 AWS EKS Managed Infrastructure & Flask App

A production-style DevOps assignment: containerized Flask on **Amazon EKS**, infrastructure as code with **Terraform**, deployment with **Helm**, and automation via **GitHub Actions**.

> **Personal twist:** S3 state backend via `bootstrap/` (no manual bucket creation) + custom dark-themed Flask UI.

---

## 🛠 Project Architecture

| Layer | Technology | Folder |
|-------|------------|--------|
| State backend | S3 | `bootstrap/` |
| Infrastructure | VPC, NAT, EKS, ECR, IAM | `Terraform/` |
| Application | Flask + Docker | `app/` |
| Orchestration | Helm → LoadBalancer | `flask-chart/` |
| CI/CD | GitHub Actions | `.github/workflows/` |

```
┌─────────────┐     ┌──────────────┐     ┌─────────┐     ┌──────────────┐
│  bootstrap  │ ──► │   Terraform   │ ──► │   ECR   │ ──► │ flask-chart  │
│  (S3 state) │     │ VPC/EKS/ECR  │     │  image  │     │  (Helm/EKS)  │
└─────────────┘     └──────────────┘     └─────────┘     └──────────────┘
                              ▲                                    │
                              │         GitHub Actions             ▼
                              └────────────────────────────────  Internet
```

### 📸 Screenshots

Place images in `docs/images/` (lowercase filenames).

| File | What to show |
|------|----------------|
| `app.png` | Flask UI in browser |
| `workflow.png` | GitHub Actions — Terraform workflow (Bonus 1) |
| `grafana.png` | Grafana — Kubernetes pods dashboard (Bonus 2) |

> Use **lowercase** filenames (`app.png` not `App.png`) for Linux/GitHub.

#### Application

![Flask application](docs/images/app.png)

#### Bonus 1 — CI/CD (Terraform workflow)

![Terraform workflow](docs/images/workflow.png)

#### Bonus 2 — Monitoring

![Grafana monitoring](docs/images/grafana.png)

---

## 🏗 Tech Stack

![Terraform](https://img.shields.io/badge/terraform-%235835CC.svg?style=for-the-badge&logo=terraform&logoColor=white)
![AWS](https://img.shields.io/badge/AWS-%23FF9900.svg?style=for-the-badge&logo=amazon-aws&logoColor=white)
![Docker](https://img.shields.io/badge/docker-%232496ed.svg?style=for-the-badge&logo=docker&logoColor=white)
![Kubernetes](https://img.shields.io/badge/kubernetes-%23326ce5.svg?style=for-the-badge&logo=kubernetes&logoColor=white)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Helm](https://img.shields.io/badge/helm-0F1689?style=for-the-badge&logo=helm&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/github%20actions-2088FF?style=for-the-badge&logo=githubactions&logoColor=white)

---

## 📋 Prerequisites

- AWS account + IAM user for CLI / CI
- [AWS CLI](https://aws.amazon.com/cli/) configured
- [Terraform](https://www.terraform.io/downloads) >= 1.0
- [kubectl](https://kubernetes.io/docs/tasks/tools/)
- [Helm](https://helm.sh/docs/intro/install/)
- [Docker](https://docs.docker.com/get-docker/)

---

## 🚀 Getting Started

| Step | Folder | Before you start | After success |
|------|--------|------------------|---------------|
| 1 | `bootstrap/` | AWS CLI configured | You have `state_bucket_name` |
| 2 | `Terraform/` | Bucket name from step 1 | EKS + ECR exist (~15 min) |
| 3 | `app/` | ECR URL from step 2 | Image pushed to ECR |
| 4 | `flask-chart/` | Image in ECR, kubeconfig set | App URL in browser |
| 5 | GitHub | Secrets configured | CI can build & deploy |

---

### 1️⃣ Backend bootstrapping

**Working directory:** `bootstrap/`

```bash
terraform init
terraform apply
```

Copy output `state_bucket_name` (e.g. `ron-devops-state-a1b2c3d4`).

> No DynamoDB — assignment requires S3 for state only.

---

### 2️⃣ Infrastructure provisioning (Terraform)

**Working directory:** `Terraform/`

```bash
terraform init -backend-config="bucket=YOUR_BUCKET_NAME"
terraform apply
```

Wait ~15 minutes. Save outputs:

```bash
terraform output cluster_name
terraform output cluster_endpoint
terraform output ecr_repository_url
terraform output node_iam_role_arn
```

**GitHub secret for CI:** `TF_STATE_BUCKET` = same bucket name.

---

### 3️⃣ Application containerization (Docker)

**Working directory:** `app/` — see [app/README.md](app/README.md)

```bash
docker build -t flask-app:latest .

aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <AWS_ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com

docker tag flask-app:latest <ECR_REPOSITORY_URL>:latest
docker push <ECR_REPOSITORY_URL>:latest
```

---

### 4️⃣ Application deployment (Helm)

**Working directory:** `flask-chart/`

```bash
aws eks update-kubeconfig --region us-east-1 --name ron-eks-mission

helm upgrade --install my-flask-app . \
  --set image.repository=<ECR_URL_WITHOUT_TAG> \
  --set image.tag=latest
```

Public URL:

```bash
kubectl get svc flask-app-service
```

Open `http://<EXTERNAL-IP>`.

---

### 5️⃣ GitHub Actions (CI/CD)

**Repository secrets:**

| Secret | Purpose |
|--------|---------|
| `AWS_ACCESS_KEY_ID` | AWS auth |
| `AWS_SECRET_ACCESS_KEY` | AWS auth |
| `TF_STATE_BUCKET` | S3 backend bucket name |

**Order matters:**

1. `bootstrap` (local) → create bucket  
2. Add `TF_STATE_BUCKET` secret  
3. Push → **Terraform Infrastructure** workflow (creates ECR + EKS)  
4. **Build and Deploy** runs after Terraform succeeds (or on `app/` / `flask-chart/` changes)

---

## 🧹 Teardown — delete everything (important order)

LoadBalancer ENIs block VPC deletion. Run from any directory where `kubectl` / `helm` work (after `aws eks update-kubeconfig`).

### Step 1 — Remove apps from Kubernetes

```bash
aws eks update-kubeconfig --region us-east-1 --name ron-eks-mission

helm uninstall my-flask-app
helm uninstall kube-prometheus -n monitoring   # skip if Bonus 2 was not installed
```

### Step 2 — Wait for LoadBalancers to disappear

```bash
kubectl get svc -A
```

Wait until `flask-app-service` and `kube-prometheus-grafana` have no `EXTERNAL-IP` (2–5 minutes).

### Step 3 — Destroy AWS infrastructure (Terraform)

**Working directory:** `Terraform/`

```bash
cd Terraform
terraform destroy
```

This removes: VPC, NAT, EKS, node groups, ECR repository (and images inside it), IAM roles created by this project.

### Step 4 — S3 state bucket (bootstrap)

The state bucket is **not** deleted by `terraform destroy`. It was created in `bootstrap/` with `prevent_destroy`.

To remove it (optional, only when you are done forever):

```bash
cd bootstrap
# First remove prevent_destroy from main.tf, then:
terraform destroy
```

Or delete the bucket manually in AWS Console → S3.

### Step 5 — Local cleanup (optional)

```bash
docker image rm flask-app:latest 2>/dev/null || true
docker image rm <AWS_ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com/ron-eks-mission-repo:latest 2>/dev/null || true
```

### Verify nothing is left billing

In AWS Console check: **EKS**, **EC2**, **VPC**, **ECR**, **Load Balancers** — all empty for this project.

---

## 🎨 Application UI

Custom dark Material Design dashboard:

| Technology | Color |
|------------|-------|
| Terraform | Purple `#844fba` |
| AWS EKS | Orange `#ff9900` |
| Docker | Blue `#2496ed` |

---

## 🎯 Bonus features

### Bonus 1 — Terraform via GitHub Actions ✅

Workflow: [`.github/workflows/terraform.yml`](.github/workflows/terraform.yml)

**What it does:** runs `terraform plan` + `terraform apply` on AWS (VPC, EKS, ECR, …).

**One-time setup (same as main project):**
1. `bootstrap` → copy `state_bucket_name`
2. GitHub secret `TF_STATE_BUCKET` = that bucket name
3. GitHub secrets `AWS_ACCESS_KEY_ID` + `AWS_SECRET_ACCESS_KEY`

**Run:** GitHub → Actions → **Terraform Infrastructure** → *Run workflow*  
(or push changes under `Terraform/`)

---

### Bonus 2 — Monitoring (Prometheus + Grafana) ✅

Config: [`monitoring/values.yaml`](monitoring/values.yaml)  
Workflow: [`.github/workflows/monitoring.yml`](.github/workflows/monitoring.yml)

**What it does:** installs `kube-prometheus-stack` — metrics for the cluster and your pods (including Flask).

**Install (pick one):**

*From your machine (WSL):*
```bash
aws eks update-kubeconfig --region us-east-1 --name ron-eks-mission
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
helm upgrade --install kube-prometheus prometheus-community/kube-prometheus-stack \
  -n monitoring --create-namespace -f monitoring/values.yaml
kubectl get svc -n monitoring kube-prometheus-grafana
```
Open `http://<EXTERNAL-IP>` → login `admin` / `admin` → screenshot for `docs/images/grafana.png`

*Or via GitHub:* Actions → **Deploy Monitoring (Bonus 2)** → *Run workflow*

> Uses extra cluster resources. Uninstall before `terraform destroy` (see Teardown).

---

## 🎯 Assignment checklist

- [x] Terraform: VPC, public + private subnets, NAT, EKS, 2 node groups, ECR, IAM  
- [x] Terraform outputs: cluster name, endpoint, ECR URL, IAM ARNs  
- [x] Dockerfile + ECR push  
- [x] Helm chart + internet access (LoadBalancer)  
- [x] GitHub Actions: build, push, deploy  
- [x] Bonus 1: Terraform workflow  
- [x] Bonus 2: Monitoring (install when ready + `grafana.png`)  
- [x] App screenshot (`app.png`)

---

## 👨‍💻 Developed By

**Ron** | DevOps Professional Course 2026
