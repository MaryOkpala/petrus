output "namespace" {
  value = kubernetes_namespace.team.metadata[0].name
}

output "quota_name" {
  value = kubernetes_resource_quota.team.metadata[0].name
}
