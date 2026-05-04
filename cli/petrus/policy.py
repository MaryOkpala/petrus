import json
import subprocess
import os
from typing import Tuple, List

POLICY_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    "policies"
)

def check_policy(request: dict) -> Tuple[bool, List[str]]:
    """Run OPA policy checks against a provisioning request."""
    violations = []

    policy_files = [
        "environments/environment.rego",
        "security/security.rego",
        "cost/cost.rego",
    ]

    packages = [
        "data.petrus.environments.deny",
        "data.petrus.security.deny",
        "data.petrus.cost.deny",
    ]

    for policy_file, query in zip(policy_files, packages):
        policy_path = os.path.join(POLICY_DIR, policy_file)

        if not os.path.exists(policy_path):
            continue

        input_data = json.dumps(request)

        try:
            result = subprocess.run(
                [
                    "opa", "eval",
                    "--data", policy_path,
                    "--input", "/dev/stdin",
                    "--format", "json",
                    query
                ],
                input=input_data,
                capture_output=True,
                text=True,
                timeout=10
            )

            if result.returncode == 0:
                output = json.loads(result.stdout)
                results = output.get("result", [])
                if results:
                    exprs = results[0].get("expressions", [])
                    if exprs:
                        denials = exprs[0].get("value", [])
                        if isinstance(denials, list):
                            violations.extend(denials)
            else:
                if result.stderr:
                    violations.append(f"Policy error in {policy_file}: {result.stderr.strip()}")

        except subprocess.TimeoutExpired:
            violations.append(f"Policy check timed out for {policy_file}")
        except Exception as e:
            violations.append(f"Policy check error: {str(e)}")

    allowed = len(violations) == 0
    return allowed, violations
