# Petrus — Operations Runbook

## What is Petrus

Petrus is an Internal Developer Platform that eliminates the bottleneck between
developers and platform teams. Developers self-service complete cloud environments
in minutes through a CLI or web portal. Every request is validated by Open Policy
Agent before anything touches AWS.

## Prerequisites

| Tool | Version |
|------|---------|
| Python | >= 3.9 |
| Terraform | >= 1.0 |
| kubectl | >= 1.28 |
| Helm | >= 3.0 |
| OPA | >= 0.60 |
| AWS CLI | >= 2.0 |

## Quick start

```bash
# Clone the repo
git clone https://github.com/MaryOkpala/petrus.git
cd petrus

# Install the CLI
pip install -e cli/

# Validate a request
petrus validate --type web-app --team payments --env dev

# Provision an environment
petrus provision --type web-app --team payments --env dev

# Check status
petrus status

# Destroy an environment
petrus destroy --team payments --env dev
```

## Start the developer portal

```bash
cd portal
pip install flask kubernetes pyyaml
python3 app.py
```

Portal runs at http://localhost:7007

## Environment types

| Type | What gets provisioned |
|------|-----------------------|
| web-app | VPC · EKS namespace · Nginx ingress · CI/CD · Prometheus |
| api | VPC · EKS namespace · service mesh · rate limiting · CI/CD |
| data-pipeline | S3 data lake · Glue ETL · Athena · cost monitoring |
| ai-ml | S3 · Glue · EMR · Athena · Redshift · SageMaker-ready |

## Policy rules

All requests are validated by OPA before provisioning.
Policy files live in policies/.

Key rules:
- t3.micro and t3.small are not allowed in prod
- S3 buckets must never be public
- SSH must not be open to 0.0.0.0/0
- All environments require cost_center tag
- Large instances require platform team approval

Run policy tests:
```bash
opa test policies/ -v
```

## Access services

| Service | URL |
|---------|-----|
| Petrus portal | http://35.174.220.243:7007 |
| ArgoCD | http://35.174.220.243:31088 |
| Grafana | http://35.174.220.243:31300 |
| Prometheus | http://35.174.220.243:31090 |
| AlertManager | http://35.174.220.243:31093 |

## Check cluster health

```bash
kubectl get nodes
kubectl get pods -A
petrus status
```

## Shutdown to save costs

```bash
sudo shutdown -h now
```

All k3s state persists across stops. Everything comes back when
the instance starts again.
