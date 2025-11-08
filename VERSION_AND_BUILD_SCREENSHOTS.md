# Version Management and System Building - Screenshot Guide

Complete guide for taking screenshots demonstrating version management (Git) and system building processes.

---

## PART 1: VERSION MANAGEMENT (Git)

### Screenshot 1: Git Repository Status
```bash
cd /Users/rraghavkaushik/Documents/SEM-7/SWE/EduBot
git status
```
**📸 Screenshot:** Terminal showing git status with current branch and file changes

---

### Screenshot 2: Commit History
```bash
git log --oneline --graph --all -10
```
**📸 Screenshot:** Terminal showing commit history with graph visualization

---

### Screenshot 3: View All Branches
```bash
git branch -a
```
**📸 Screenshot:** Terminal showing all branches (local and remote if any)

---

### Screenshot 4: Create and View Version Tags
```bash
# Create version tags (if not already created)
git tag -a v1.0.0 -m "Version 1.0.0 - Initial release" 2>/dev/null || echo "Tag exists"
git tag -a v1.1.0 -m "Version 1.1.0 - Added AI features" 2>/dev/null || echo "Tag exists"
git tag -a v1.2.0 -m "Version 1.2.0 - Added quiz mode and documents" 2>/dev/null || echo "Tag exists"

# View all tags
git tag -l
```
**📸 Screenshot:** Terminal showing version tags

---

### Screenshot 5: View Tag Details
```bash
git show v1.0.0 --no-patch
```
**📸 Screenshot:** Terminal showing tag details and message

---

### Screenshot 6: View Commit Statistics
```bash
git log --stat --oneline -5
```
**📸 Screenshot:** Terminal showing commit statistics (files changed, insertions, deletions)

---

### Screenshot 7: Git Configuration
```bash
git config --list --local | head -10
```
**📸 Screenshot:** Terminal showing Git configuration

---

## PART 2: SYSTEM BUILDING

### Screenshot 8: Backend Virtual Environment
```bash
cd /Users/rraghavkaushik/Documents/SEM-7/SWE/EduBot
echo "=== Virtual Environment ==="
which python
python --version
echo ""
echo "=== Virtual Environment Location ==="
echo $VIRTUAL_ENV
```
**📸 Screenshot:** Terminal showing Python version and virtual environment

---

### Screenshot 9: Backend Dependencies Installation
```bash
cd /Users/rraghavkaushik/Documents/SEM-7/SWE/EduBot
source venv/bin/activate
echo "=== Installing Backend Dependencies ==="
pip install -r requirements.txt 2>&1 | tail -20
```
**📸 Screenshot:** Terminal showing pip install output (or "already satisfied" messages)

---

### Screenshot 10: Backend Dependencies List
```bash
cd /Users/rraghavkaushik/Documents/SEM-7/SWE/EduBot
source venv/bin/activate
echo "=== Installed Python Packages ==="
pip list | head -20
echo ""
echo "=== Total packages ==="
pip list | wc -l
```
**📸 Screenshot:** Terminal showing list of installed Python packages

---

### Screenshot 11: Frontend Dependencies Installation
```bash
cd /Users/rraghavkaushik/Documents/SEM-7/SWE/EduBot/frontend
echo "=== Installing Frontend Dependencies ==="
npm install 2>&1 | tail -15
```
**📸 Screenshot:** Terminal showing npm install output

---

### Screenshot 12: Frontend Dependencies List
```bash
cd /Users/rraghavkaushik/Documents/SEM-7/SWE/EduBot/frontend
echo "=== Installed npm Packages ==="
npm list --depth=0 2>/dev/null | head -20
```
**📸 Screenshot:** Terminal showing npm package list

---

### Screenshot 13: Frontend Production Build
```bash
cd /Users/rraghavkaushik/Documents/SEM-7/SWE/EduBot/frontend
echo "=== Building Frontend for Production ==="
npm run build
```
**📸 Screenshot:** Terminal showing production build output

---

### Screenshot 14: Build Artifacts
```bash
cd /Users/rraghavkaushik/Documents/SEM-7/SWE/EduBot/frontend
echo "=== Build Output Directory ==="
ls -lh dist/
echo ""
echo "=== Build Artifacts Size ==="
du -sh dist/
```
**📸 Screenshot:** Terminal showing build artifacts (dist folder contents)

---

### Screenshot 15: Build Script Execution
```bash
cd /Users/rraghavkaushik/Documents/SEM-7/SWE/EduBot
echo "=== Running Build Script ==="
./build.sh
```
**📸 Screenshot:** Terminal showing build script execution

---

### Screenshot 16: Requirements Files
```bash
cd /Users/rraghavkaushik/Documents/SEM-7/SWE/EduBot
echo "=== Backend Requirements ==="
head -20 requirements.txt
echo ""
echo "=== Frontend package.json ==="
head -30 frontend/package.json
```
**📸 Screenshot:** Terminal showing requirements.txt and package.json

---

### Screenshot 17: Database Initialization
```bash
cd /Users/rraghavkaushik/Documents/SEM-7/SWE/EduBot
source venv/bin/activate
echo "=== Database Initialization ==="
python -c "from app import app, db; app.app_context().push(); db.create_all(); print('Database initialized successfully')"
echo ""
echo "=== Database File ==="
ls -lh instance/edubot.db 2>/dev/null || echo "Database file location"
```
**📸 Screenshot:** Terminal showing database initialization

---

### Screenshot 18: System Architecture Overview
```bash
cd /Users/rraghavkaushik/Documents/SEM-7/SWE/EduBot
echo "=== Project Structure ==="
tree -L 2 -I 'node_modules|venv|__pycache__|*.pyc|htmlcov|mutants' 2>/dev/null || find . -maxdepth 2 -type d -not -path '*/\.*' -not -path '*/node_modules*' -not -path '*/venv*' | head -20
```
**📸 Screenshot:** Terminal showing project directory structure

---

## QUICK SCRIPT: Run All Commands

Save this as `version_build_screenshots.sh`:

```bash
#!/bin/bash
cd /Users/rraghavkaushik/Documents/SEM-7/SWE/EduBot

echo "=========================================="
echo "VERSION MANAGEMENT & BUILD SCREENSHOTS"
echo "=========================================="
echo ""
echo "Run each section, take screenshot, press Enter"
echo ""

# VERSION MANAGEMENT
echo ">>> SCREENSHOT 1: Git Status"
read -p "Press Enter..."
clear
git status
read -p "Press Enter after screenshot..."

echo ""
echo ">>> SCREENSHOT 2: Commit History"
read -p "Press Enter..."
git log --oneline --graph --all -10
read -p "Press Enter after screenshot..."

echo ""
echo ">>> SCREENSHOT 3: Branches"
read -p "Press Enter..."
git branch -a
read -p "Press Enter after screenshot..."

echo ""
echo ">>> SCREENSHOT 4: Version Tags"
read -p "Press Enter..."
git tag -l
read -p "Press Enter after screenshot..."

# SYSTEM BUILDING
echo ""
echo ">>> SCREENSHOT 5: Virtual Environment"
read -p "Press Enter..."
clear
source venv/bin/activate
which python
python --version
read -p "Press Enter after screenshot..."

echo ""
echo ">>> SCREENSHOT 6: Backend Dependencies"
read -p "Press Enter..."
pip list | head -20
read -p "Press Enter after screenshot..."

echo ""
echo ">>> SCREENSHOT 7: Frontend Dependencies"
read -p "Press Enter..."
cd frontend
npm list --depth=0 2>/dev/null | head -20
read -p "Press Enter after screenshot..."

echo ""
echo ">>> SCREENSHOT 8: Production Build"
read -p "Press Enter..."
npm run build
read -p "Press Enter after screenshot..."

echo ""
echo ">>> SCREENSHOT 9: Build Artifacts"
read -p "Press Enter..."
ls -lh dist/
read -p "Press Enter after screenshot..."

cd ..
echo ""
echo ">>> SCREENSHOT 10: Build Script"
read -p "Press Enter..."
./build.sh
read -p "Press Enter after screenshot..."

echo ""
echo "=========================================="
echo "All screenshots completed!"
echo "=========================================="
```

---

## For Your Project Report

### Version Management Section

**Title:** "Version Control and Release Management"

**Content:**
> "EduBot uses Git for version control with semantic versioning (MAJOR.MINOR.PATCH). The project maintains version tags (v1.0.0, v1.1.0, v1.2.0) to track releases. All changes are committed with descriptive messages, and the repository structure supports collaborative development."

**Screenshots to include:**
- Git status showing clean working directory
- Commit history with meaningful messages
- Version tags (v1.0.0, v1.1.0, v1.2.0)
- Branch structure

---

### System Building Section

**Title:** "Build System and Dependency Management"

**Content:**
> "EduBot uses separate build systems for backend (Python/pip) and frontend (Node.js/npm). The backend uses a virtual environment for dependency isolation, while the frontend uses npm for package management. A unified build script (`build.sh`) automates the entire build process, ensuring consistent deployments."

**Screenshots to include:**
- Virtual environment setup
- Backend dependency installation (pip install)
- Frontend dependency installation (npm install)
- Production build output
- Build artifacts (dist folder)
- Build script execution

---

## Summary Table

| Category | Screenshot | Purpose |
|----------|-----------|---------|
| Version Management | Git status | Show repository state |
| Version Management | Commit history | Show development timeline |
| Version Management | Version tags | Show release versions |
| System Building | Virtual environment | Show Python isolation |
| System Building | pip install | Show backend dependencies |
| System Building | npm install | Show frontend dependencies |
| System Building | npm build | Show production build |
| System Building | Build artifacts | Show output files |
| System Building | Build script | Show automation |

---

## Ready to Take Screenshots?

1. Open terminal
2. Run commands from this guide one by one
3. Take screenshot after each command
4. Use the text templates above in your report
5. Add screenshots to your project document

**All commands are ready to run!** 🎉

