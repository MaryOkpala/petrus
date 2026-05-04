resource "aws_security_group" "app" {
  name        = "${var.project}-${var.team}-${var.environment}-app-sg"
  description = "Application security group for ${var.team} ${var.environment}"
  vpc_id      = var.vpc_id

  ingress {
    description = "HTTP from public subnet"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "HTTPS from public subnet"
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "App port from VPC"
    from_port   = 8080
    to_port     = 8080
    protocol    = "tcp"
    cidr_blocks = [var.vpc_cidr]
  }

  egress {
    description = "Allow all outbound"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name        = "${var.project}-${var.team}-${var.environment}-app-sg"
    Project     = var.project
    Team        = var.team
    Environment = var.environment
    ManagedBy   = "Petrus"
    CostCenter  = var.team
  }
}

resource "aws_iam_role" "app" {
  name = "${var.project}-${var.team}-${var.environment}-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = {
        Service = "ec2.amazonaws.com"
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

resource "aws_iam_role_policy_attachment" "ssm" {
  role       = aws_iam_role.app.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore"
}
