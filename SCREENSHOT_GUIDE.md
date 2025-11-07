# Screenshot Guide for Project Submission

This guide provides step-by-step instructions for taking screenshots of integration/regression/mutation testing and version management/system building.

## Prerequisites

1. Ensure all dependencies are installed:
```bash
pip install -r test_requirements.txt
cd frontend && npm install && cd ..
```

2. Make scripts executable:
```bash
chmod +x run_all_tests.sh
chmod +x build.sh
```

## Part 1: Integration Testing Screenshots

### Screenshot 1: Integration Test Execution
```bash
pytest test_integration.py -v --tb=short
```
**What to capture:**
- Terminal showing test execution
- All tests passing (green checkmarks)
- Test names showing integration scenarios

### Screenshot 2: Integration Test Results
```bash
pytest test_integration.py -v --tb=short | tail -20
```
**What to capture:**
- Summary showing passed/failed tests
- Test coverage information

## Part 2: Regression Testing Screenshots

### Screenshot 3: Regression Test Execution
```bash
pytest test_regression.py -v --tb=short
```
**What to capture:**
- All regression tests passing
- Test names indicating regression scenarios

### Screenshot 4: Regression Test Summary
```bash
pytest test_regression.py -v --tb=short --co
```
**What to capture:**
- Test count and results
- Coverage percentage

## Part 3: Mutation Testing Screenshots

### Screenshot 5: Mutation Testing Setup
```bash
pip install mutmut
mutmut run
```
**What to capture:**
- Mutation testing execution
- Mutations being tested

### Screenshot 6: Mutation Testing Results
```bash
mutmut results
```
**What to capture:**
- Mutation score (survival rate)
- Number of mutations killed/survived

### Screenshot 7: Mutation Details
```bash
mutmut show <mutation-id>
```
**What to capture:**
- Example of a mutation
- Code changes made by mutmut

## Part 4: Version Management Screenshots

### Screenshot 8: Git Status
```bash
git status
```
**What to capture:**
- Clean working directory
- Branch name

### Screenshot 9: Git Log/History
```bash
git log --oneline --graph --all -10
```
**What to capture:**
- Commit history
- Branch structure
- Commit messages

### Screenshot 10: Version Tags
```bash
git tag -l
git show v1.0.0
```
**What to capture:**
- List of version tags
- Tag details with annotations

### Screenshot 11: Branch Structure
```bash
git branch -a
git log --graph --oneline --all
```
**What to capture:**
- All branches
- Branch relationships

### Screenshot 12: Version Comparison
```bash
git diff v1.0.0 v1.1.0 --stat
```
**What to capture:**
- Files changed between versions
- Statistics

## Part 5: System Building Screenshots

### Screenshot 13: Backend Dependencies
```bash
source venv/bin/activate
pip list
```
**What to capture:**
- List of installed packages
- Versions

### Screenshot 14: Frontend Dependencies
```bash
cd frontend
npm list --depth=0
```
**What to capture:**
- npm package list
- Dependency tree

### Screenshot 15: Build Process
```bash
cd frontend
npm run build
```
**What to capture:**
- Build output
- Success message
- Build artifacts

### Screenshot 16: Build Artifacts
```bash
ls -la frontend/dist
```
**What to capture:**
- Built files
- File sizes
- Directory structure

### Screenshot 17: Dependency Tree
```bash
pip install pipdeptree
pipdeptree
```
**What to capture:**
- Dependency relationships
- Package hierarchy

## Quick Script to Generate All Screenshots

```bash
#!/bin/bash
# screenshot_all.sh - Generate all screenshots

echo "Taking screenshots for project submission..."

# Integration tests
echo "1. Integration tests..."
pytest test_integration.py -v > integration_tests.txt

# Regression tests
echo "2. Regression tests..."
pytest test_regression.py -v > regression_tests.txt

# Mutation tests
echo "3. Mutation tests..."
mutmut run > mutation_tests.txt 2>&1
mutmut results >> mutation_tests.txt

# Version management
echo "4. Version management..."
git status > git_status.txt
git log --oneline --graph --all -10 > git_log.txt
git tag -l > git_tags.txt

# Build system
echo "5. Build system..."
source venv/bin/activate
pip list > pip_list.txt
cd frontend && npm list --depth=0 > ../npm_list.txt && cd ..

echo "All outputs saved to text files. Take screenshots of these files or terminal."
```

## Screenshot Checklist

### Integration/Regression/Mutation Testing
- [ ] Integration test execution
- [ ] Integration test results
- [ ] Regression test execution
- [ ] Regression test results
- [ ] Mutation testing execution
- [ ] Mutation testing results
- [ ] Mutation score/survival rate

### Version Management
- [ ] Git status
- [ ] Git commit history
- [ ] Version tags
- [ ] Branch structure
- [ ] Version comparison

### System Building
- [ ] Backend dependencies (pip list)
- [ ] Frontend dependencies (npm list)
- [ ] Build process execution
- [ ] Build artifacts
- [ ] Dependency tree

## Tips for Good Screenshots

1. **Use full-screen terminal** for better visibility
2. **Highlight important information** with terminal colors
3. **Include command prompts** to show what was executed
4. **Show complete output** (scroll to show all results)
5. **Use consistent terminal theme** across screenshots
6. **Add annotations** if needed (arrows, boxes)

## Example Terminal Commands for Screenshots

```bash
# Clear terminal and show command
clear
echo "=== Integration Tests ==="
pytest test_integration.py -v

# Wait for screenshot
read -p "Press Enter after taking screenshot..."

clear
echo "=== Regression Tests ==="
pytest test_regression.py -v

# Continue for all screenshots...
```

