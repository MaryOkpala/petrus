terraform {
  required_providers {
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = "~> 2.0"
    }
  }
}

resource "kubernetes_namespace" "team" {
  metadata {
    name = "${var.team}-${var.environment}"

    labels = {
      team        = var.team
      environment = var.environment
      managed-by  = "petrus"
      cost-center = var.team
    }

    annotations = {
      "petrus.io/team"        = var.team
      "petrus.io/environment" = var.environment
      "petrus.io/type"        = var.environment_type
    }
  }
}

resource "kubernetes_resource_quota" "team" {
  metadata {
    name      = "${var.team}-${var.environment}-quota"
    namespace = kubernetes_namespace.team.metadata[0].name
  }

  spec {
    hard = {
      "requests.cpu"    = var.cpu_request_limit
      "requests.memory" = var.memory_request_limit
      "limits.cpu"      = var.cpu_limit
      "limits.memory"   = var.memory_limit
      "pods"            = var.pod_limit
    }
  }
}

resource "kubernetes_role" "team" {
  metadata {
    name      = "${var.team}-${var.environment}-role"
    namespace = kubernetes_namespace.team.metadata[0].name
  }

  rule {
    api_groups = ["", "apps", "batch"]
    resources  = ["pods", "deployments", "services", "configmaps", "jobs"]
    verbs      = ["get", "list", "watch", "create", "update", "patch", "delete"]
  }
}

resource "kubernetes_role_binding" "team" {
  metadata {
    name      = "${var.team}-${var.environment}-binding"
    namespace = kubernetes_namespace.team.metadata[0].name
  }

  role_ref {
    api_group = "rbac.authorization.k8s.io"
    kind      = "Role"
    name      = kubernetes_role.team.metadata[0].name
  }

  subject {
    kind = "Group"
    name = var.team
  }
}
