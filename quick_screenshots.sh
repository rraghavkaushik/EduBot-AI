#!/bin/bash
# Quick script to run commands for screenshots

echo "=========================================="
echo "EduBot Screenshot Helper"
echo "=========================================="
echo ""
echo "This script will run commands for you to screenshot."
echo "Press Enter after each command to continue..."
echo ""

# Activate venv
source venv/bin/activate 2>/dev/null

# Integration Tests
echo "=== INTEGRATION TESTS ==="
echo "Command: pytest test_integration.py -v"
read -p "Press Enter to run integration tests..."
pytest test_integration.py -v --tb=short
echo ""
read -p "Press Enter after taking screenshot..."

# Regression Tests
echo ""
echo "=== REGRESSION TESTS ==="
echo "Command: pytest test_regression.py -v"
read -p "Press Enter to run regression tests..."
pytest test_regression.py -v --tb=short
echo ""
read -p "Press Enter after taking screenshot..."

# Mutation Tests
echo ""
echo "=== MUTATION TESTS ==="
echo "Command: mutmut run"
read -p "Press Enter to run mutation tests (this may take a while)..."
mutmut run 2>&1 | head -50
echo ""
read -p "Press Enter after taking screenshot..."

echo ""
echo "Command: mutmut results"
read -p "Press Enter to show mutation results..."
mutmut results
echo ""
read -p "Press Enter after taking screenshot..."

# Version Management
echo ""
echo "=== VERSION MANAGEMENT ==="
echo "Command: git status"
read -p "Press Enter to show git status..."
git status
echo ""
read -p "Press Enter after taking screenshot..."

echo ""
echo "Command: git log --oneline --graph --all -10"
read -p "Press Enter to show git log..."
git log --oneline --graph --all -10
echo ""
read -p "Press Enter after taking screenshot..."

echo ""
echo "Command: git tag -l"
read -p "Press Enter to show version tags..."
git tag -l || echo "No tags yet. Create one with: git tag -a v1.0.0 -m 'Version 1.0.0'"
echo ""
read -p "Press Enter after taking screenshot..."

# Build System
echo ""
echo "=== BUILD SYSTEM ==="
echo "Command: pip list"
read -p "Press Enter to show Python packages..."
pip list | head -20
echo ""
read -p "Press Enter after taking screenshot..."

echo ""
echo "Command: cd frontend && npm list --depth=0"
read -p "Press Enter to show npm packages..."
cd frontend && npm list --depth=0 2>/dev/null | head -20
cd ..
echo ""
read -p "Press Enter after taking screenshot..."

echo ""
echo "Command: npm run build (in frontend/)"
read -p "Press Enter to build frontend..."
cd frontend && npm run build
cd ..
echo ""
read -p "Press Enter after taking screenshot..."

echo ""
echo "=========================================="
echo "All screenshot commands completed!"
echo "=========================================="

