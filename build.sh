#!/bin/bash
# Build script for EduBot

echo "=========================================="
echo "EduBot Build System"
echo "=========================================="
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Backend setup
echo -e "${BLUE}1. Setting up backend environment...${NC}"
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

source venv/bin/activate
echo "Installing backend dependencies..."
pip install -r requirements.txt
echo -e "${GREEN}✓ Backend dependencies installed${NC}"
echo ""

# Frontend setup
echo -e "${BLUE}2. Setting up frontend environment...${NC}"
cd frontend
if [ ! -d "node_modules" ]; then
    echo "Installing frontend dependencies..."
    npm install
fi
echo -e "${GREEN}✓ Frontend dependencies installed${NC}"
echo ""

# Production build
echo -e "${BLUE}3. Building frontend for production...${NC}"
npm run build
echo -e "${GREEN}✓ Frontend build complete${NC}"
cd ..
echo ""

# Database initialization
echo -e "${BLUE}4. Initializing database...${NC}"
python -c "from app import app, db; app.app_context().push(); db.create_all()" 2>/dev/null
echo -e "${GREEN}✓ Database initialized${NC}"
echo ""

echo -e "${GREEN}=========================================="
echo "Build Complete!"
echo "==========================================${NC}"

