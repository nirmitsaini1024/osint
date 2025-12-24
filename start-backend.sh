#!/bin/bash

# Start the FastAPI backend server

cd "$(dirname "$0")/sherlock"

# Activate virtual environment
source venv/bin/activate

# Start the server
echo "Starting FastAPI server on http://localhost:8000"
python api.py

