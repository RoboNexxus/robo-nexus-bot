#!/bin/bash
set -e  # Exit on error

echo "🚀 Starting Robo Nexus Bot..."
echo "================================"

# Check Python version
echo "🐍 Python version:"
python3 --version

# Install dependencies
echo ""
echo "📦 Installing dependencies..."
pip3 install --upgrade pip
pip3 install -r requirements.txt

# Check if installation was successful
if [ $? -eq 0 ]; then
    echo "✅ Dependencies installed successfully"
else
    echo "❌ Failed to install dependencies"
    exit 1
fi

# Start the bot
echo ""
echo "🤖 Starting bot..."
echo "================================"
python3 main.py