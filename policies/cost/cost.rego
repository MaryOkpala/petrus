package petrus.cost

large_instance_types := {
  "m5.2xlarge",
  "m5.4xlarge",
  "c5.2xlarge",
  "c5.4xlarge",
  "r5.large",
  "r5.xlarge",
  "p3.2xlarge",
  "g4dn.xlarge"
}

deny[msg] {
  input.instance_type == large_instance_types[_]
  not input.approved
  msg := sprintf(
    "Instance type '%v' requires platform team approval.",
    [input.instance_type]
  )
}

deny[msg] {
  input.current_environment_count >= 5
  msg := sprintf(
    "Team '%v' has reached the maximum of 5 environments.",
    [input.team]
  )
}

deny[msg] {
  not input.tags.cost_center
  msg := "All Petrus environments require a cost_center tag for billing attribution."
}

deny[msg] {
  input.instance_type == "p3.2xlarge"
  input.environment_type != "ai-ml"
  msg := "GPU instances are only allowed in ai-ml environment type."
}

warn[msg] {
  input.environment == "dev"
  input.nat_gateway == true
  msg := "NAT gateway in dev costs ~$1/day even when idle."
}
