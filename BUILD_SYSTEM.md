# System Building Guide

This guide shows how to build and package the EduBot system.

## Backend Build System

### 1. Virtual Environment Setup
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```
**Screenshot:** Terminal showing dependency installation

### 2. Database Initialization
```bash
python -c "from app import app, db; app.app_context().push(); db.create_all()"
```
**Screenshot:** Terminal showing database creation

### 3. Environment Configuration
```bash
# Show environment setup
cat > .env.example << 'EOF'
GEMINI_API_KEY=your-api-key-here
JWT_SECRET_KEY=your-secret-key
DATABASE_URL=sqlite:///edubot.db
PORT=5001
EOF

cat .env.example
```
**Screenshot:** Terminal showing environment configuration

## Frontend Build System

### 1. Install Dependencies
```bash
cd frontend
npm install
```
**Screenshot:** Terminal showing npm install

### 2. Development Build
```bash
npm run dev
```
**Screenshot:** Terminal showing dev server running

### 3. Production Build
```bash
npm run build
```
**Screenshot:** Terminal showing production build

### 4. View Build Output
```bash
ls -la frontend/dist
```
**Screenshot:** Terminal showing build artifacts

## Build Scripts

### Create build.sh
```bash
cat > build.sh << 'EOF'
#!/bin/bash
echo "Building EduBot..."

# Backend
echo "1. Setting up backend..."
source venv/bin/activate
pip install -r requirements.txt

# Frontend
echo "2. Building frontend..."
cd frontend
npm install
npm run build
cd ..

echo "Build complete!"
EOF

chmod +x build.sh
```

**Screenshot:** Terminal showing build script execution

## Package Management

### Backend Dependencies
```bash
pip list
pip freeze > requirements-lock.txt
```
**Screenshot:** Terminal showing Python packages

### Frontend Dependencies
```bash
cd frontend
npm list --depth=0
```
**Screenshot:** Terminal showing npm packages

## System Architecture

### Dependency Graph
```bash
# Backend
pip install pipdeptree
pipdeptree

# Frontend
cd frontend
npm install -g npm-remote-ls
npm-remote-ls
```
**Screenshot:** Terminal showing dependency trees

## Build Screenshots Checklist

- [ ] Virtual environment creation
- [ ] Dependency installation (pip install)
- [ ] Dependency installation (npm install)
- [ ] Production build output
- [ ] Build artifacts (dist folder)
- [ ] Dependency tree/graph
- [ ] Environment configuration
- [ ] Build script execution

## Docker Build (Optional)

If using Docker:
```bash
# Create Dockerfile
cat > Dockerfile << 'EOF'
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "app.py"]
EOF

# Build Docker image
docker build -t edubot:latest .
```
**Screenshot:** Terminal showing Docker build

