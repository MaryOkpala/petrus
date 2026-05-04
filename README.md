# Petrus — Internal Developer Platform

> Self-service cloud infrastructure for development teams. Provision a production-ready environment in 5 minutes. Zero tickets. Policy-enforced by default.

## The problem

Developers wait days for platform teams to provision environments. Platform teams spend their expertise on repetitive tickets instead of building better systems. Security policies get ignored because they are manual. Cloud costs are invisible until the bill arrives.

## The solution

Petrus eliminates the bottleneck. Developers self-service everything they need through a portal or CLI. Platform teams define guardrails once using Open Policy Agent — no request can bypass them. Every environment is provisioned identically from Terraform modules, deployed via ArgoCD GitOps, and monitored automatically with Prometheus and Grafana.

## What Petrus provisions

| Environment type | What you get |
|-----------------|-------------|
| Web app | VPC · EKS namespace · Nginx ingress · CI/CD pipeline · Prometheus monitoring |
| API service | VPC · EKS namespace · service mesh · rate limiting · CI/CD pipeline |
| Data pipeline | S3 data lake · Glue ETL · Athena · cost monitoring |
| AI/ML workload | S3 · Glue · EMR · Athena · Redshift · SageMaker-ready |

## Stack

| Layer | Tools |
|-------|-------|
| Developer portal | Backstage |
| Policy enforcement | Open Policy Agent (OPA) |
| Infrastructure provisioning | Terraform · Crossplane |
| GitOps delivery | ArgoCD |
| Kubernetes | k3s · Helm |
| Observability | Prometheus · Grafana · AlertManager |
| CLI | Python |
| Cloud | AWS |

## Repository structure
petrus/
├── cli/                    # Python CLI — petrus provision / destroy / status
├── portal/                 # Backstage developer portal
├── terraform/
│   ├── modules/            # Reusable infrastructure modules
│   └── environments/       # Environment templates
├── policies/               # OPA policy rules
├── argocd/                 # ArgoCD application manifests
├── monitoring/             # Prometheus rules and Grafana dashboards
├── docs/                   # Architecture and runbooks
└── scripts/                # Utility scripts
## Quick start

```bash
# Install the CLI
pip install -e cli/

# Provision a web app environment
petrus provision --type web-app --team payments --env staging

# Check environment status
petrus status --team payments

# Destroy environment
petrus destroy --team payments --env staging
```

## Status

Currently in active development. Follow along on GitHub.
