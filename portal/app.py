from flask import Flask, render_template, request, jsonify, redirect, url_for
import subprocess
import json
import os
import yaml
from datetime import datetime

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ENVIRONMENT_TYPES = ["web-app", "api", "data-pipeline", "ai-ml"]
ENVIRONMENT_NAMES = ["dev", "staging", "prod"]
REGIONS = ["us-east-1", "us-west-2", "ca-central-1"]

MOCK_ENVIRONMENTS = [
    {
        "team": "payments",
        "environment": "dev",
        "type": "web-app",
        "namespace": "payments-dev",
        "status": "Healthy",
        "pods": "3/3",
        "region": "us-east-1",
        "age": "2d",
        "argocd": "http://35.174.220.243:31088/applications/payments-dev",
        "grafana": "http://35.174.220.243:31300/d/payments-dev",
        "created": "2026-04-28"
    },
    {
        "team": "data-science",
        "environment": "staging",
        "type": "ai-ml",
        "namespace": "data-science-staging",
        "status": "Healthy",
        "pods": "2/2",
        "region": "us-east-1",
        "age": "5h",
        "argocd": "http://35.174.220.243:31088/applications/data-science-staging",
        "grafana": "http://35.174.220.243:31300/d/data-science-staging",
        "created": "2026-04-30"
    },
    {
        "team": "platform",
        "environment": "prod",
        "type": "api",
        "namespace": "platform-prod",
        "status": "Healthy",
        "pods": "4/4",
        "region": "us-east-1",
        "age": "7d",
        "argocd": "http://35.174.220.243:31088/applications/platform-prod",
        "grafana": "http://35.174.220.243:31300/d/platform-prod",
        "created": "2026-04-23"
    }
]

SERVICES = [
    {
        "name": "Petrus CLI",
        "team": "platform-team",
        "type": "tool",
        "lifecycle": "production",
        "description": "Command line interface for self-service environment provisioning",
        "repo": "https://github.com/MaryOkpala/petrus",
        "tags": ["cli", "python", "devops"]
    },
    {
        "name": "Payments API",
        "team": "payments-team",
        "type": "service",
        "lifecycle": "experimental",
        "description": "Core payments processing API provisioned via Petrus",
        "repo": "https://github.com/MaryOkpala/petrus",
        "tags": ["api", "payments", "web-app"]
    },
    {
        "name": "Data Science Pipeline",
        "team": "data-science-team",
        "type": "service",
        "lifecycle": "experimental",
        "description": "AI/ML data pipeline using Petrus ai-ml environment template",
        "repo": "https://github.com/MaryOkpala/petrus",
        "tags": ["ai", "ml", "data-pipeline"]
    },
    {
        "name": "Platform API",
        "team": "platform-team",
        "type": "service",
        "lifecycle": "production",
        "description": "Internal platform API for developer tooling",
        "repo": "https://github.com/MaryOkpala/petrus",
        "tags": ["api", "platform", "internal"]
    }
]

def run_policy_check(data):
    """Run OPA policy check against a request."""
    policy_files = [
        ("environments/environment.rego", "data.petrus.environments.deny"),
        ("security/security.rego", "data.petrus.security.deny"),
        ("cost/cost.rego", "data.petrus.cost.deny"),
    ]
    violations = []
    policies_dir = os.path.join(BASE_DIR, "policies")

    for policy_file, query in policy_files:
        policy_path = os.path.join(policies_dir, policy_file)
        if not os.path.exists(policy_path):
            continue
        try:
            result = subprocess.run(
                ["opa", "eval", "--data", policy_path,
                 "--input", "/dev/stdin", "--format", "json", query],
                input=json.dumps(data),
                capture_output=True, text=True, timeout=10
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
        except Exception as e:
            violations.append(f"Policy check error: {str(e)}")

    return len(violations) == 0, violations

@app.route("/")
def index():
    return render_template("index.html",
        environments=MOCK_ENVIRONMENTS,
        services=SERVICES,
        total_envs=len(MOCK_ENVIRONMENTS),
        healthy=sum(1 for e in MOCK_ENVIRONMENTS if e["status"] == "Healthy"),
        teams=len(set(e["team"] for e in MOCK_ENVIRONMENTS))
    )

@app.route("/environments")
def environments():
    team_filter = request.args.get("team", "")
    envs = MOCK_ENVIRONMENTS
    if team_filter:
        envs = [e for e in envs if e["team"] == team_filter]
    teams = list(set(e["team"] for e in MOCK_ENVIRONMENTS))
    return render_template("environments.html",
        environments=envs,
        teams=teams,
        selected_team=team_filter
    )

@app.route("/provision", methods=["GET", "POST"])
def provision():
    if request.method == "POST":
        data = request.form
        req = {
            "environment_type": data.get("env_type"),
            "team": data.get("team"),
            "environment": data.get("environment"),
            "region": data.get("region", "us-east-1"),
            "instance_type": data.get("instance_type", "t3.medium"),
            "approved": False,
            "nat_gateway": data.get("environment") != "dev",
            "current_environment_count": 0,
            "tags": {
                "team": data.get("team"),
                "environment": data.get("environment"),
                "cost_center": data.get("team")
            }
        }
        allowed, violations = run_policy_check(req)
        return render_template("provision_result.html",
            allowed=allowed,
            violations=violations,
            request=req
        )
    return render_template("provision.html",
        env_types=ENVIRONMENT_TYPES,
        env_names=ENVIRONMENT_NAMES,
        regions=REGIONS
    )

@app.route("/catalog")
def catalog():
    return render_template("catalog.html", services=SERVICES)

@app.route("/api/environments")
def api_environments():
    return jsonify(MOCK_ENVIRONMENTS)

@app.route("/api/health")
def api_health():
    return jsonify({
        "status": "healthy",
        "platform": "Petrus IDP",
        "version": "0.1.0",
        "timestamp": datetime.utcnow().isoformat()
    })

@app.route("/api/validate", methods=["POST"])
def api_validate():
    data = request.get_json()
    allowed, violations = run_policy_check(data)
    return jsonify({
        "allowed": allowed,
        "violations": violations
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7007, debug=False)
