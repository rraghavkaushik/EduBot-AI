# Step-by-Step Guide: Taking Testing Screenshots for Project

Follow these steps **one by one** to take screenshots for your project submission.

## Prerequisites

Make sure you're in the project directory:
```bash
cd /Users/rraghavkaushik/Documents/SEM-7/SWE/EduBot
source venv/bin/activate
```

---

## STEP 1: Integration Testing Screenshot

### Command to run:
```bash
clear
echo "=== INTEGRATION TESTING ==="
pytest test_integration.py -v
```

### What to screenshot:
- Full terminal window
- Show all 6 tests passing
- Test names visible (registration, login, upload, AI, workflow, database)

### What to write in your report:
> "Integration testing verifies that different components work together. We test user registration→login flow, file upload with text extraction, AI features with authentication, end-to-end workflows, and database relationships. All 6 integration tests pass successfully."

**Press Enter after taking screenshot, then continue...**

---

## STEP 2: Integration Test Summary

### Command to run:
```bash
pytest test_integration.py -v --tb=line | tail -5
```

### What to screenshot:
- Summary showing "6 passed"
- Total execution time

**Press Enter after taking screenshot, then continue...**

---

## STEP 3: Regression Testing Screenshot

### Command to run:
```bash
clear
echo "=== REGRESSION TESTING ==="
pytest test_regression.py -v
```

### What to screenshot:
- Full terminal window
- Show all regression tests
- Test names showing what's being tested (API endpoints, authentication, file upload, AI, data models)
- Pass/fail status

### What to write in your report:
> "Regression testing ensures existing functionality continues to work after code changes. We test all API endpoints, authentication security, file upload functionality, AI features, and data model structure. Our regression suite contains 14 tests covering critical functionality."

**Press Enter after taking screenshot, then continue...**

---

## STEP 4: Regression Test Summary

### Command to run:
```bash
pytest test_regression.py -v --tb=line | tail -5
```

### What to screenshot:
- Summary showing passed/failed counts
- Overall statistics

**Press Enter after taking screenshot, then continue...**

---

## STEP 5: Mutation Testing Configuration

### Command to run:
```bash
clear
echo "=== MUTATION TESTING CONFIGURATION ==="
cat setup.cfg
```

### What to screenshot:
- Configuration file showing paths_to_mutate
- Shows mutation testing is configured

**Press Enter after taking screenshot, then continue...**

---

## STEP 6: Mutation Testing Execution

### Command to run:
```bash
clear
echo "=== MUTATION TESTING EXECUTION ==="
echo "Running mutations (this may take 1-2 minutes)..."
mutmut run 2>&1 | head -30
```

### What to screenshot:
- Terminal showing mutation testing starting
- Mutations being tested
- Progress information

**Note:** If this takes too long, you can interrupt after 30 seconds and explain that mutation testing runs all mutations.

**Press Enter after taking screenshot, then continue...**

---

## STEP 7: Mutation Testing Results

### Command to run:
```bash
mutmut results
```

### What to screenshot:
- Mutation score
- Number of mutations killed vs survived
- Example: "X mutations tested, Y killed, Z survived"

### What to write in your report:
> "Mutation testing evaluates test quality by introducing small code changes. A high kill rate (mutations caught by tests) indicates strong test coverage. Our mutation testing targets the main application code and shows that our test suite effectively detects code changes."

**Press Enter after taking screenshot, then continue...**

---

## STEP 8: Test Coverage Report

### Command to run:
```bash
clear
echo "=== TEST COVERAGE ==="
pytest --cov=app --cov-report=term-missing --cov-report=html
echo ""
echo "Coverage report generated. Opening in browser..."
open htmlcov/index.html
```

### What to screenshot:
- Terminal showing coverage percentage
- Browser showing HTML coverage report (if it opens)
- Files and coverage percentages

### What to write in your report:
> "Code coverage analysis shows that X% of our codebase is covered by tests. The coverage report identifies which lines are tested and which need additional test coverage."

**Press Enter after taking screenshot, then continue...**

---

## STEP 9: All Tests Summary

### Command to run:
```bash
clear
echo "=== COMPLETE TEST SUITE SUMMARY ==="
echo ""
echo "Unit Tests:"
pytest test_app.py -v --tb=no -q
echo ""
echo "Integration Tests:"
pytest test_integration.py -v --tb=no -q
echo ""
echo "Regression Tests:"
pytest test_regression.py -v --tb=no -q
```

### What to screenshot:
- Summary of all test suites
- Total test counts
- Overall pass/fail status

**Press Enter after taking screenshot, then continue...**

---

## STEP 10: Test Files Overview

### Command to run:
```bash
clear
echo "=== TEST FILES STRUCTURE ==="
ls -lh test_*.py
echo ""
echo "=== TEST FILE SIZES ==="
wc -l test_*.py
```

### What to screenshot:
- List of test files
- Line counts showing test suite size
- Demonstrates comprehensive testing

**Press Enter after taking screenshot, then continue...**

---

## How to Use These Screenshots in Your Report

### 1. Create a "Testing" Section

Structure it like this:

```
## Testing Methodology

### Integration Testing
[Screenshot 1: Integration test execution]
[Screenshot 2: Integration test summary]

**Explanation:**
Integration testing verifies that different components of EduBot work together correctly. 
Our integration test suite includes:
- User registration and login flow
- File upload with text extraction
- AI features with authentication
- End-to-end user workflows
- Database relationships

All 6 integration tests pass successfully, demonstrating proper component integration.

### Regression Testing
[Screenshot 3: Regression test execution]
[Screenshot 4: Regression test summary]

**Explanation:**
Regression testing ensures that existing functionality continues to work after code changes.
Our regression test suite covers:
- API endpoint functionality
- Authentication security
- File upload validation
- AI feature consistency
- Data model structure

14 regression tests ensure backward compatibility and system stability.

### Mutation Testing
[Screenshot 5: Configuration]
[Screenshot 6: Execution]
[Screenshot 7: Results]

**Explanation:**
Mutation testing evaluates test quality by introducing small code changes (mutations).
A high mutation kill rate indicates strong test coverage. Our mutation testing targets
the main application code and demonstrates that our test suite effectively detects
code changes.

### Test Coverage
[Screenshot 8: Coverage report]

**Explanation:**
Code coverage analysis shows X% of our codebase is covered by tests, ensuring
comprehensive testing of critical functionality.
```

### 2. Add a Testing Summary Table

| Test Type | Number of Tests | Status | Purpose |
|-----------|----------------|--------|---------|
| Unit Tests | X | ✅ Passing | Test individual components |
| Integration Tests | 6 | ✅ Passing | Test component interactions |
| Regression Tests | 14 | ✅ Passing | Ensure backward compatibility |
| Mutation Tests | X mutations | X% kill rate | Evaluate test quality |

### 3. Key Points to Emphasize

- **Comprehensive Coverage**: Multiple test types ensure quality
- **Automated Testing**: All tests can be run automatically
- **Continuous Validation**: Tests ensure code changes don't break functionality
- **Quality Assurance**: Mutation testing validates test effectiveness

---

## Quick Reference: All Commands in Order

```bash
# 1. Integration Tests
pytest test_integration.py -v

# 2. Integration Summary
pytest test_integration.py -v --tb=line | tail -5

# 3. Regression Tests
pytest test_regression.py -v

# 4. Regression Summary
pytest test_regression.py -v --tb=line | tail -5

# 5. Mutation Config
cat setup.cfg

# 6. Mutation Execution
mutmut run 2>&1 | head -30

# 7. Mutation Results
mutmut results

# 8. Coverage Report
pytest --cov=app --cov-report=term-missing --cov-report=html

# 9. All Tests Summary
pytest test_app.py test_integration.py test_regression.py -v --tb=no -q

# 10. Test Files
ls -lh test_*.py && wc -l test_*.py
```

---

## Tips for Professional Presentation

1. **Use consistent terminal theme** across all screenshots
2. **Clear terminal before each command** for clean screenshots
3. **Show command prompts** to indicate what was executed
4. **Highlight important numbers** (test counts, percentages)
5. **Add labels/annotations** in your report document
6. **Group related screenshots** together in your report
7. **Include brief explanations** with each screenshot

---

## Example Report Text Template

Copy and adapt this for your project:

> **Testing Strategy**
> 
> EduBot employs a comprehensive testing strategy including unit, integration, regression, and mutation testing to ensure software quality and reliability.
> 
> **Integration Testing**
> Integration tests verify that different system components work together correctly. Our test suite includes 6 integration tests covering user authentication flows, file upload with text extraction, AI feature integration, end-to-end workflows, and database relationships. All integration tests pass successfully, demonstrating proper component integration.
> 
> **Regression Testing**
> Regression tests ensure that existing functionality continues to work after code changes. Our regression test suite contains 14 test cases covering API endpoints, authentication mechanisms, file upload functionality, AI features, and data models. This ensures backward compatibility and system stability as the codebase evolves.
> 
> **Mutation Testing**
> Mutation testing evaluates the quality of our test suite by introducing small code changes (mutations) and verifying that tests can detect these changes. A high mutation kill rate indicates strong test coverage. Our mutation testing is configured to target the main application code, and results demonstrate that our test suite effectively catches code changes.
> 
> **Test Coverage**
> Code coverage analysis shows that X% of our codebase is covered by automated tests, ensuring comprehensive testing of critical functionality including authentication, file processing, and AI integration.

