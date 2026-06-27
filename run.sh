#!/bin/bash

# AI Healthcare Chatbot - Quick Start Script
# This script sets up and runs the application

echo "🏥 AI Healthcare Chatbot - Quick Start"
echo "======================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is not installed"
    echo "   Please install Python 3.8 or higher"
    exit 1
fi

echo "✓ Python 3 is installed"

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ Error: pip is not installed"
    echo "   Please install pip"
    exit 1
fi

echo "✓ pip is installed"

# Install dependencies
echo ""
echo "📦 Installing dependencies..."
pip3 install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ Error: Failed to install dependencies"
    exit 1
fi

echo "✓ Dependencies installed"

# Setup database with sample data
echo ""
echo "🗄️  Setting up database with sample data..."
python3 setup.py

if [ $? -ne 0 ]; then
    echo "❌ Error: Failed to setup database"
    exit 1
fi

# Run the application
echo ""
echo "🚀 Starting the application..."
echo "   Access at: http://localhost:5000"
echo "   Press Ctrl+C to stop"
echo ""

python3 app.py
