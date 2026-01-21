#!/bin/bash

# Go to the folder of this script
cd "$(dirname "$0")"

# Activate virtual environment
source venv/bin/activate

# Start Flask in background
python3 web_site.py &
FLASK_PID=$!

# Run Cloudflare Tunnel (reads config.yml automatically)
cloudflared tunnel run calorietracker

# When tunnel stops, kill Flask
kill $FLASK_PID
