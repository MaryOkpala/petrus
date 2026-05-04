#!/bin/bash
echo "Stopping Petrus portal..."
pkill -f "python3 app.py" || true
echo "Portal stopped."
echo "Run 'sudo shutdown -h now' to stop the EC2 instance."
