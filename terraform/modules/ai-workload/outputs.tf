output "data_lake_bucket" {
  value = aws_s3_bucket.data_lake.bucket
}

output "glue_database" {
  value = aws_glue_catalog_database.main.name
}

output "athena_workgroup" {
  value = aws_athena_workgroup.main.name
}

output "glue_role_arn" {
  value = aws_iam_role.glue.arn
}
