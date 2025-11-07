# Testing Guide for EduBot

This guide explains how to run different types of tests and take screenshots for your project submission.

## Test Types

### 1. Unit Tests (`test_app.py`)
Tests individual components in isolation.

**Run:**
```bash
pytest test_app.py -v
```

**Screenshot:** Terminal showing test results with coverage

### 2. Integration Tests (`test_integration.py`)
Tests interaction between multiple components.

**Run:**
```bash
pytest test_integration.py -v
```

**Screenshot:** Terminal showing integration test results

### 3. Regression Tests (`test_regression.py`)
Ensures existing functionality still works after changes.

**Run:**
```bash
pytest test_regression.py -v
```

**Screenshot:** Terminal showing regression test results

### 4. Mutation Testing (`mutmut`)
Tests the quality of your test suite by introducing small changes (mutations) to your code.

**Setup:**
```bash
pip install mutmut
```

**Run:**
```bash
mutmut run
```

**View results:**
```bash
mutmut results
```

**Screenshot:** Terminal showing mutation test results

## Running All Tests

```bash
chmod +x run_all_tests.sh
./run_all_tests.sh
```

## Coverage Report

Generate HTML coverage report:
```bash
pytest --cov=app --cov-report=html
open htmlcov/index.html
```

**Screenshot:** Browser showing coverage report

## Test Screenshots Checklist

- [ ] Unit tests passing
- [ ] Integration tests passing
- [ ] Regression tests passing
- [ ] Mutation testing results
- [ ] Coverage report (HTML)
- [ ] Test execution summary

