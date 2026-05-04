# ArgoCD Application Manifests

Petrus generates ArgoCD Application manifests dynamically when a developer
provisions an environment. Each environment gets its own Application resource
that watches a dedicated path in this repository.

## How it works

1. Developer runs: `petrus provision --type web-app --team payments --env dev`
2. Petrus creates: `environments/payments/dev/` in this repo
3. Petrus applies: `argocd/payments-dev.yaml` to the cluster
4. ArgoCD syncs: all manifests from `environments/payments/dev/` to the `payments-dev` namespace
5. Developer pushes changes to `environments/payments/dev/` and ArgoCD auto-deploys

## Template

See `petrus-app-template.yaml` for the Application resource template.
Petrus substitutes TEAM and ENVIRONMENT at provision time.

## Current applications

Run `kubectl get applications -n argocd` to see all active environments.
