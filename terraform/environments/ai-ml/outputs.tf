output "vpc_id"           { value = module.networking.vpc_id }
output "app_sg_id"        { value = module.security.app_sg_id }
output "data_lake"        { value = module.ai_workload.data_lake_bucket }
output "glue_database"    { value = module.ai_workload.glue_database }
output "athena_workgroup" { value = module.ai_workload.athena_workgroup }
output "glue_role_arn"    { value = module.ai_workload.glue_role_arn }
