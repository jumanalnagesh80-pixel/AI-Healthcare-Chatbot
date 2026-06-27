#!/bin/bash

# ═══════════════════════════════════════════════════════════
#  🏥 AI Healthcare Chatbot - Easy Setup Script
# ═══════════════════════════════════════════════════════════

echo ""
echo "╔═══════════════════════════════════════════════════════════╗"
echo "║   🏥 AI Healthcare Chatbot - Automated Setup             ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Step counter
STEP=1

print_step() {
    echo ""
    echo -e "${BLUE}[Step $STEP/$1]${NC} $2"
    ((STEP++))
}

print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

# Total steps
TOTAL_STEPS=6

echo "This script will automatically:"
echo "  • Check Python installation"
echo "  • Install dependencies"
echo "  • Setup database"
echo "  • Verify installation"
echo "  • Run tests (optional)"
echo "  • Start the application"
echo ""
read -p "Press Enter to continue or Ctrl+C to cancel..."
echo ""

# ═══════════════════════════════════════════════════════════
# Step 1: Check Python
# ═══════════════════════════════════════════════════════════
print_step $TOTAL_STEPS "Checking Python installation"

if command -v python3 &> /dev/null; then
    PYTHON_CMD=python3
    PYTHON_VERSION=$(python3 --version)
    print_success "Python found: $PYTHON_VERSION"
elif command -v python &> /dev/null; then
    PYTHON_CMD=python
    PYTHON_VERSION=$(python --version)
    print_success "Python found: $PYTHON_VERSION"
else
    print_error "Python not found! Please install Python 3.7 or higher"
    exit 1
fi

# ═══════════════════════════════════════════════════════════
# Step 2: Check pip
# ═══════════════════════════════════════════════════════════
print_step $TOTAL_STEPS "Checking pip installation"

if command -v pip3 &> /dev/null; then
    PIP_CMD=pip3
    print_success "pip3 found"
elif command -v pip &> /dev/null; then
    PIP_CMD=pip
    print_success "pip found"
else
    print_error "pip not found! Please install pip"
    exit 1
fi

# ═══════════════════════════════════════════════════════════
# Step 3: Install dependencies
# ═══════════════════════════════════════════════════════════
print_step $TOTAL_STEPS "Installing Python dependencies"

echo "Installing packages from requirements_modern.txt..."
if $PIP_CMD install -r requirements_modern.txt > /dev/null 2>&1; then
    print_success "Dependencies installed successfully"
else
    print_warning "Some packages may have failed to install. Trying again..."
    $PIP_CMD install -r requirements_modern.txt
fi

# ═══════════════════════════════════════════════════════════
# Step 4: Setup database
# ═══════════════════════════════════════════════════════════
print_step $TOTAL_STEPS "Setting up database"

if [ -f "healthcare.db" ]; then
    print_warning "Database already exists. Skipping setup."
else
    echo "Running database setup..."
    if $PYTHON_CMD setup_enhanced.py > /dev/null 2>&1; then
        print_success "Database created"
    else
        print_warning "Database setup had warnings (this may be normal)"
    fi
fi

# Add health goals table
echo "Adding health goals table..."
if $PYTHON_CMD add_health_goals_table.py > /dev/null 2>&1; then
    print_success "Health goals table added"
else
    print_warning "Health goals table may already exist"
fi

# ═══════════════════════════════════════════════════════════
# Step 5: Verify installation
# ═══════════════════════════════════════════════════════════
print_step $TOTAL_STEPS "Verifying installation"

# Check if main files exist
files_to_check=(
    "app_modern.py"
    "ai_medical_knowledge.py"
    "database.py"
    "static/css/modern.css"
    "static/js/enhanced.js"
    "templates/index_modern.html"
)

all_good=true
for file in "${files_to_check[@]}"; do
    if [ -f "$file" ]; then
        print_success "Found: $file"
    else
        print_error "Missing: $file"
        all_good=false
    fi
done

if [ "$all_good" = false ]; then
    print_error "Some files are missing! Installation may be incomplete."
    exit 1
fi

# ═══════════════════════════════════════════════════════════
# Step 6: Optional - Run tests
# ═══════════════════════════════════════════════════════════
print_step $TOTAL_STEPS "Running tests (optional)"

echo ""
read -p "Do you want to run tests? (y/n) " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "Running test suite..."
    if command -v pytest &> /dev/null; then
        pytest tests/ -v --tb=short
    else
        print_warning "pytest not installed. Skipping tests."
        echo "To run tests later: pytest tests/ -v"
    fi
else
    echo "Skipping tests. You can run them later with: pytest tests/ -v"
fi

# ═══════════════════════════════════════════════════════════
# Setup Complete!
# ═══════════════════════════════════════════════════════════

echo ""
echo "╔═══════════════════════════════════════════════════════════╗"
echo "║              ✓ Setup Complete! 🎉                        ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""

print_success "All components installed and configured!"
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  📚 Quick Start Guide"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "1. Start the application:"
echo "   ${GREEN}$PYTHON_CMD app_modern.py${NC}"
echo ""
echo "2. Open your browser:"
echo "   ${GREEN}http://localhost:5000${NC}"
echo ""
echo "3. Register a new account and start using the chatbot!"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  📖 Documentation"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "  • START_HERE.md      - Complete user guide"
echo "  • README_FINAL.md    - Technical documentation"
echo "  • VISUAL_GUIDE.md    - UI/UX guide"
echo "  • PROJECT_COMPLETE.txt - Feature summary"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  🧪 Testing"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "  Run tests: ${GREEN}pytest tests/ -v${NC}"
echo "  With coverage: ${GREEN}pytest tests/ --cov=.${NC}"
echo "  Test script: ${GREEN}bash run_tests.sh${NC}"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  🚀 Ready to start?"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
read -p "Start the application now? (y/n) " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo ""
    echo "🚀 Starting AI Healthcare Chatbot..."
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "  Application running at: http://localhost:5000"
    echo "  Press Ctrl+C to stop"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    $PYTHON_CMD app_modern.py
else
    echo ""
    echo "No problem! When you're ready, run:"
    echo "  ${GREEN}$PYTHON_CMD app_modern.py${NC}"
    echo ""
fi

echo ""
echo "Thank you for using AI Healthcare Chatbot! 🏥"
echo ""
