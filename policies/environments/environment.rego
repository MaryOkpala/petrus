package petrus.environments

valid_environment_types := {
  "web-app",
  "api",
  "data-pipeline",
  "ai-ml"
}

valid_environment_names := {
  "dev",
  "staging",
  "prod"
}

valid_regions := {
  "us-east-1",
  "us-west-2",
  "ca-central-1"
}

allowed_instance_types := {
  "dev":     {"t3.micro", "t3.small", "t3.medium"},
  "staging": {"t3.small", "t3.medium", "t3.large"},
  "prod":    {"t3.medium", "t3.large", "m5.large", "m5.xlarge"}
}

allow {
  valid_environment_type
  valid_environment_name
  valid_region
  valid_instance_type
  has_required_tags
}

valid_environment_type {
  input.environment_type == valid_environment_types[_]
}

valid_environment_name {
  input.environment == valid_environment_names[_]
}

valid_region {
  input.region == valid_regions[_]
}

valid_instance_type {
  input.instance_type == allowed_instance_types[input.environment][_]
}

has_required_tags {
  input.tags.team != ""
  input.tags.environment != ""
  input.tags.cost_center != ""
}

deny[msg] {
  not valid_environment_type
  msg := sprintf(
    "Invalid environment type '%v'. Must be one of: web-app, api, data-pipeline, ai-ml",
    [input.environment_type]
  )
}

deny[msg] {
  not valid_environment_name
  msg := sprintf(
    "Invalid environment name '%v'. Must be one of: dev, staging, prod",
    [input.environment]
  )
}

deny[msg] {
  not valid_region
  msg := sprintf(
    "Region '%v' is not allowed. Petrus provisions into: us-east-1, us-west-2, ca-central-1",
    [input.region]
  )
}

deny[msg] {
  valid_environment_name
  not valid_instance_type
  msg := sprintf(
    "Instance type '%v' is not allowed in '%v' environment.",
    [input.instance_type, input.environment]
  )
}

deny[msg] {
  not has_required_tags
  msg := "Missing required tags. All environments must have: team, environment, cost_center"
}
