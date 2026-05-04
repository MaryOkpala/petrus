resource "aws_s3_bucket" "data_lake" {
  bucket = "${var.project}-${var.team}-${var.environment}-datalake"

  tags = {
    Name        = "${var.project}-${var.team}-${var.environment}-datalake"
    Project     = var.project
    Team        = var.team
    Environment = var.environment
    ManagedBy   = "Petrus"
    CostCenter  = var.team
    Purpose     = "ai-data-lake"
  }
}

resource "aws_s3_bucket_versioning" "data_lake" {
  bucket = aws_s3_bucket.data_lake.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "data_lake" {
  bucket = aws_s3_bucket.data_lake.id
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_public_access_block" "data_lake" {
  bucket                  = aws_s3_bucket.data_lake.id
  block_public_acls       = true
  ignore_public_acls      = true
  block_public_policy     = true
  restrict_public_buckets = true
}

resource "aws_glue_catalog_database" "main" {
  name        = "${var.team}_${var.environment}_catalog"
  description = "Glue catalog for ${var.team} ${var.environment} AI workloads"
}

resource "aws_athena_workgroup" "main" {
  name = "${var.project}-${var.team}-${var.environment}"

  configuration {
    result_configuration {
      output_location = "s3://${aws_s3_bucket.data_lake.bucket}/athena-results/"
    }
  }

  tags = {
    Project     = var.project
    Team        = var.team
    Environment = var.environment
    ManagedBy   = "Petrus"
    CostCenter  = var.team
  }
}

resource "aws_iam_role" "glue" {
  name = "${var.project}-${var.team}-${var.environment}-glue-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = {
        Service = "glue.amazonaws.com"
      }
    }]
  })

  tags = {
    Project     = var.project
    Team        = var.team
    Environment = var.environment
    ManagedBy   = "Petrus"
    CostCenter  = var.team
  }
}

resource "aws_iam_role_policy_attachment" "glue_service" {
  role       = aws_iam_role.glue.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSGlueServiceRole"
}

resource "aws_iam_role_policy" "glue_s3" {
  name = "${var.project}-${var.team}-${var.environment}-glue-s3"
  role = aws_iam_role.glue.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Action = [
        "s3:GetObject",
        "s3:PutObject",
        "s3:DeleteObject",
        "s3:ListBucket"
      ]
      Resource = [
        aws_s3_bucket.data_lake.arn,
        "${aws_s3_bucket.data_lake.arn}/*"
      ]
    }]
  })
}
