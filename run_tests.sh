#!/bin/bash
# Run tests for AI Healthcare Chatbot

echo "================================"
echo "AI Healthcare Chatbot - Test Suite"
echo "================================"
echo ""

# Check if pytest is installed
if ! command -v pytest &> /dev/null; then
    echo "❌ pytest not found. Installing test dependencies..."
    pip install -r requirements_modern.txt
    pip install pytest pytest-flask pytest-cov
fi

echo "Running tests..."
echo ""

# Run all tests with coverage
pytest tests/ -v --tb=short

echo ""
echo "================================"
echo "Test run complete!"
echo "================================"
