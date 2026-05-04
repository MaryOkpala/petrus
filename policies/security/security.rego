package petrus.security

deny[msg] {
  input.resource_type == "aws_s3_bucket"
  input.public_access == true
  msg := "S3 buckets must never be public. Petrus enforces private-only S3 access."
}

deny[msg] {
  input.resource_type == "aws_security_group"
  rule := input.ingress_rules[_]
  rule.from_port <= 22
  rule.to_port >= 22
  rule.cidr == "0.0.0.0/0"
  msg := "SSH port 22 must not be open to 0.0.0.0/0. Restrict to specific CIDR or bastion SG."
}

deny[msg] {
  input.resource_type == "aws_security_group"
  rule := input.ingress_rules[_]
  rule.from_port <= 3389
  rule.to_port >= 3389
  rule.cidr == "0.0.0.0/0"
  msg := "RDP port 3389 must not be open to 0.0.0.0/0."
}

deny[msg] {
  input.resource_type == "aws_s3_bucket"
  input.encryption_enabled == false
  msg := "S3 buckets must have server-side encryption enabled."
}

deny[msg] {
  input.resource_type == "aws_db_instance"
  input.storage_encrypted == false
  msg := "RDS instances must have storage encryption enabled."
}

deny[msg] {
  input.resource_type == "aws_instance"
  input.environment == "prod"
  input.instance_type == "t3.micro"
  msg := "Instance type t3.micro is not suitable for production."
}

deny[msg] {
  input.environment == "prod"
  input.instance_type == "t3.micro"
  msg := "Instance type t3.micro is not allowed in prod environment. Use t3.medium or larger."
}

deny[msg] {
  input.environment == "prod"
  input.instance_type == "t3.small"
  msg := "Instance type t3.small is not allowed in prod environment. Use t3.medium or larger."
}
