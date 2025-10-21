#!/bin/bash
# Image Encryption App - Quick Start Script

echo "🔐 Image Encryption Application"
echo "================================"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Please run setup first."
    echo "Creating virtual environment..."
    python3 -m venv venv
    source venv/bin/activate
    pip install cryptography Pillow
    echo "✅ Virtual environment created and dependencies installed"
else
    echo "✅ Virtual environment found"
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Check if tkinter is available
echo "Checking GUI dependencies..."
python3 -c "import tkinter" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "❌ tkinter not available. Please install python-tk:"
    echo "brew install python-tk"
    exit 1
fi

echo "✅ All dependencies ready"

# Run the application
echo ""
echo "🚀 Starting Image Encryption GUI..."
echo "=================================="
python3 gui_app.py
