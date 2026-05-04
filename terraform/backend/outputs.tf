output "state_bucket" {
  description = "S3 state bucket name"
  value       = aws_s3_bucket.state.bucket
}

output "lock_table" {
  description = "DynamoDB lock table name"
  value       = aws_dynamodb_table.locks.name
}
