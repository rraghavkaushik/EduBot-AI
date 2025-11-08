#!/bin/bash
# Script to run commands for taking testing screenshots
# Run each section, take screenshot, then press Enter to continue

cd /Users/rraghavkaushik/Documents/SEM-7/SWE/EduBot
source venv/bin/activate

echo ""
echo "=========================================="
echo "TESTING SCREENSHOTS FOR PROJECT"
echo "=========================================="
echo ""
echo "Run each command, take screenshot, then press Enter"
echo ""

# 1. Integration Tests
echo ">>> SCREENSHOT 1: Integration Testing"
read -p "Press Enter to run integration tests..."
clear
echo "=== INTEGRATION TESTING ==="
echo ""
pytest test_integration.py -v
echo ""
read -p "Press Enter after taking screenshot..."

# 2. Integration Summary
echo ""
echo ">>> SCREENSHOT 2: Integration Test Summary"
read -p "Press Enter to show summary..."
pytest test_integration.py -v --tb=line | tail -8
read -p "Press Enter after taking screenshot..."

# 3. Regression Tests
echo ""
echo ">>> SCREENSHOT 3: Regression Testing"
read -p "Press Enter to run regression tests..."
clear
echo "=== REGRESSION TESTING ==="
echo ""
pytest test_regression.py -v
echo ""
read -p "Press Enter after taking screenshot..."

# 4. Regression Summary
echo ""
echo ">>> SCREENSHOT 4: Regression Test Summary"
read -p "Press Enter to show summary..."
pytest test_regression.py -v --tb=line | tail -8
read -p "Press Enter after taking screenshot..."

# 5. Mutation Config
echo ""
echo ">>> SCREENSHOT 5: Mutation Testing Configuration"
read -p "Press Enter to show configuration..."
clear
echo "=== MUTATION TESTING CONFIGURATION ==="
echo ""
cat setup.cfg
read -p "Press Enter after taking screenshot..."

# 6. Mutation Execution
echo ""
echo ">>> SCREENSHOT 6: Mutation Testing Execution"
read -p "Press Enter to run mutation tests (may take time)..."
clear
echo "=== MUTATION TESTING EXECUTION ==="
echo "Running mutations (showing first 40 lines)..."
echo ""
mutmut run 2>&1 | head -40
echo ""
echo "... (mutation testing continues in background)"
read -p "Press Enter after taking screenshot..."

# 7. Mutation Results
echo ""
echo ">>> SCREENSHOT 7: Mutation Testing Results"
read -p "Press Enter to show results..."
mutmut results
read -p "Press Enter after taking screenshot..."

# 8. Coverage
echo ""
echo ">>> SCREENSHOT 8: Test Coverage"
read -p "Press Enter to show coverage..."
clear
echo "=== TEST COVERAGE ==="
echo ""
pytest --cov=app --cov-report=term-missing
read -p "Press Enter after taking screenshot..."

# 9. All Tests Summary
echo ""
echo ">>> SCREENSHOT 9: Complete Test Suite"
read -p "Press Enter to show all tests summary..."
clear
echo "=== COMPLETE TEST SUITE SUMMARY ==="
echo ""
pytest test_app.py test_integration.py test_regression.py -v --tb=no -q
read -p "Press Enter after taking screenshot..."

echo ""
echo "=========================================="
echo "All screenshots completed!"
echo "Check TESTING_FOR_PROJECT.md for report text"
echo "=========================================="

