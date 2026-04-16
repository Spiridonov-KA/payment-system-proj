#!/bin/bash
set -e

echo "Activating virtual environment..."
source venv/bin/activate

echo "Installing dependencies..."
pip install -q -r requirements.txt

echo "Running tests..."
pytest tests/ -v --tb=short

echo "Done."