#!/bin/bash

# Exit on error
set -e

# Create and activate a virtual environment
echo "Creating virtual environment..."
python -m venv venv
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -e .

# Run the app
echo "Running the app..."
python run_app.py