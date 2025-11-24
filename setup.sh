#!/bin/bash
# Simple installation and setup script

echo "=================================================="
echo "🎨 Stable Diffusion Image Generator - Setup"
echo "=================================================="
echo ""

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed!"
    echo "   Please install Python 3.8 or higher"
    exit 1
fi

echo "✅ Python found: $(python3 --version)"
echo ""

# Create virtual environment
echo "📦 Creating virtual environment..."
if [ ! -d ".venv" ]; then
    python3 -m venv .venv
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment already exists"
fi
echo ""

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source .venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip -q

# Install requirements
echo "📥 Installing dependencies..."
echo "   (This may take several minutes)"
pip install -r requirements.txt

echo ""
echo "✅ Installation complete!"
echo ""

# Run tests
echo "🧪 Running installation tests..."
python test_installation.py

echo ""
echo "=================================================="
echo "✨ Setup Complete!"
echo "=================================================="
echo ""
echo "To run the application:"
echo "  1. Activate virtual environment: source .venv/bin/activate"
echo "  2. Run the app: python src/main.py"
echo ""
echo "Or use: ./run.sh (if available)"
echo ""
