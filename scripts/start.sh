#!/bin/bash
set -e

echo "Starting Petrus platform..."

echo "Checking k3s..."
sudo systemctl start k3s
kubectl get nodes

echo "Starting developer portal..."
cd /home/ubuntu/petrus/portal
nohup python3 app.py > /tmp/petrus-portal.log 2>&1 &
echo "Portal running at http://localhost:7007"

echo "Petrus is ready."
echo ""
echo "  Portal:     http://35.174.220.243:7007"
echo "  ArgoCD:     http://35.174.220.243:31088"
echo "  Grafana:    http://35.174.220.243:31300"
echo "  Prometheus: http://35.174.220.243:31090"
