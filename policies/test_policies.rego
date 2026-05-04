package petrus.test

import data.petrus.environments
import data.petrus.security
import data.petrus.cost

test_valid_web_app_allowed {
  environments.allow with input as {
    "environment_type": "web-app",
    "environment": "dev",
    "region": "us-east-1",
    "instance_type": "t3.medium",
    "tags": {
      "team": "payments",
      "environment": "dev",
      "cost_center": "payments"
    }
  }
}

test_invalid_env_type_denied {
  count(environments.deny) > 0 with input as {
    "environment_type": "random-thing",
    "environment": "dev",
    "region": "us-east-1",
    "instance_type": "t3.small",
    "tags": {
      "team": "payments",
      "environment": "dev",
      "cost_center": "payments"
    }
  }
}

test_public_s3_denied {
  count(security.deny) > 0 with input as {
    "resource_type": "aws_s3_bucket",
    "public_access": true,
    "encryption_enabled": true
  }
}

test_ssh_open_denied {
  count(security.deny) > 0 with input as {
    "resource_type": "aws_security_group",
    "ingress_rules": [{
      "from_port": 22,
      "to_port": 22,
      "cidr": "0.0.0.0/0"
    }]
  }
}

test_missing_cost_center_denied {
  count(cost.deny) > 0 with input as {
    "team": "payments",
    "environment": "dev",
    "instance_type": "t3.small",
    "tags": {
      "team": "payments",
      "environment": "dev"
    }
  }
}

test_large_instance_no_approval_denied {
  count(cost.deny) > 0 with input as {
    "team": "payments",
    "environment": "prod",
    "instance_type": "m5.4xlarge",
    "approved": false,
    "tags": {
      "team": "payments",
      "environment": "prod",
      "cost_center": "payments"
    }
  }
}
