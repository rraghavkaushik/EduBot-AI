#!/bin/bash
# Interactive script for taking version management and build system screenshots

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
echo "=== Git Repository Status ==="
git status
read -p "Press Enter after taking screenshot..."

echo ""
echo ">>> SCREENSHOT 2: Commit History"
read -p "Press Enter..."
clear
echo "=== Commit History ==="
git log --oneline --graph --all -10
read -p "Press Enter after taking screenshot..."

echo ""
echo ">>> SCREENSHOT 3: Branches"
read -p "Press Enter..."
clear
echo "=== Git Branches ==="
git branch -a
read -p "Press Enter after taking screenshot..."

echo ""
echo ">>> SCREENSHOT 4: Version Tags"
read -p "Press Enter..."
clear
echo "=== Version Tags ==="
# Create tags if they don't exist
git tag -a v1.0.0 -m "Version 1.0.0 - Initial release" 2>/dev/null
git tag -a v1.1.0 -m "Version 1.1.0 - Added AI features" 2>/dev/null
git tag -a v1.2.0 -m "Version 1.2.0 - Added quiz mode and documents" 2>/dev/null
git tag -l
read -p "Press Enter after taking screenshot..."

echo ""
echo ">>> SCREENSHOT 5: Tag Details"
read -p "Press Enter..."
clear
echo "=== Version Tag Details ==="
git show v1.0.0 --no-patch
read -p "Press Enter after taking screenshot..."

# SYSTEM BUILDING
echo ""
echo ">>> SCREENSHOT 6: Virtual Environment"
read -p "Press Enter..."
clear
echo "=== Python Virtual Environment ==="
source venv/bin/activate
which python
python --version
echo ""
echo "Virtual Environment: $VIRTUAL_ENV"
read -p "Press Enter after taking screenshot..."

echo ""
echo ">>> SCREENSHOT 7: Backend Dependencies List"
read -p "Press Enter..."
clear
echo "=== Installed Python Packages ==="
pip list | head -25
echo ""
echo "Total packages: $(pip list | wc -l | tr -d ' ')"
read -p "Press Enter after taking screenshot..."

echo ""
echo ">>> SCREENSHOT 8: Backend Requirements File"
read -p "Press Enter..."
clear
echo "=== requirements.txt ==="
head -25 requirements.txt
read -p "Press Enter after taking screenshot..."

echo ""
echo ">>> SCREENSHOT 9: Frontend Dependencies"
read -p "Press Enter..."
clear
echo "=== npm Package List ==="
cd frontend
npm list --depth=0 2>/dev/null | head -25
read -p "Press Enter after taking screenshot..."

echo ""
echo ">>> SCREENSHOT 10: Frontend package.json"
read -p "Press Enter..."
clear
echo "=== package.json (dependencies) ==="
cat package.json | grep -A 20 '"dependencies"'
read -p "Press Enter after taking screenshot..."

echo ""
echo ">>> SCREENSHOT 11: Production Build"
read -p "Press Enter..."
clear
echo "=== Building Frontend for Production ==="
npm run build
read -p "Press Enter after taking screenshot..."

echo ""
echo ">>> SCREENSHOT 12: Build Artifacts"
read -p "Press Enter..."
clear
echo "=== Build Output Directory ==="
ls -lh dist/
echo ""
echo "Total size: $(du -sh dist/ | cut -f1)"
read -p "Press Enter after taking screenshot..."

cd ..
echo ""
echo ">>> SCREENSHOT 13: Build Script Execution"
read -p "Press Enter..."
clear
echo "=== Running Build Script ==="
./build.sh
read -p "Press Enter after taking screenshot..."

echo ""
echo ">>> SCREENSHOT 14: Project Structure"
read -p "Press Enter..."
clear
echo "=== Project Directory Structure ==="
find . -maxdepth 2 -type d -not -path '*/\.*' -not -path '*/node_modules*' -not -path '*/venv*' -not -path '*/__pycache__*' -not -path '*/mutants*' | sort | head -25
read -p "Press Enter after taking screenshot..."

echo ""
echo "=========================================="
echo "All screenshots completed!"
echo "Check VERSION_AND_BUILD_SCREENSHOTS.md for report text"
echo "=========================================="

