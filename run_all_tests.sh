#!/bin/bash
# Run all test suites for EduBot

echo "=========================================="
echo "EduBot Test Suite Runner"
echo "=========================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Activate virtual environment
source venv/bin/activate

echo -e "${BLUE}1. Running Unit Tests...${NC}"
echo "----------------------------------------"
pytest test_app.py -v --tb=short --cov=app --cov-report=term-missing
echo ""

echo -e "${BLUE}2. Running Integration Tests...${NC}"
echo "----------------------------------------"
pytest test_integration.py -v --tb=short
echo ""

echo -e "${BLUE}3. Running Regression Tests...${NC}"
echo "----------------------------------------"
pytest test_regression.py -v --tb=short
echo ""

echo -e "${GREEN}All tests completed!${NC}"
echo ""
echo "To run mutation testing, use: mutmut run"

