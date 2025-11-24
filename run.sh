#!/bin/bash
# Quick run script - activates venv and launches the app

cd "$(dirname "$0")"

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "   Run ./setup.sh first"
    exit 1
fi

# Activate virtual environment
source .venv/bin/activate

# Check if dependencies are installed
if ! python -c "import torch" 2>/dev/null; then
    echo "❌ Dependencies not installed!"
    echo "   Run ./setup.sh first"
    exit 1
fi

# Launch the app
echo "🚀 Starting Stable Diffusion Image Generator..."
echo ""
python src/main.py
