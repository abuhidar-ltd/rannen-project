#!/bin/bash
# Script to run the Image Encryption Tool executable

echo "🔐 Starting Image Encryption Tool..."
echo "=================================="

# Check if the app exists
if [ ! -d "dist/ImageEncryptionTool.app" ]; then
    echo "❌ Executable not found. Please build it first with PyInstaller."
    exit 1
fi

# Open the macOS app
echo "🚀 Launching ImageEncryptionTool.app..."
open "dist/ImageEncryptionTool.app"

echo "✅ Application started!"
echo ""
echo "Note: If this is your first time running the app, macOS may ask for permission"
echo "to run it since it's not code-signed. You can allow it in System Preferences."

