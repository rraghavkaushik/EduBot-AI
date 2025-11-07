# Version Management Guide

This guide shows version management using Git and semantic versioning.

## Git Setup

### Initialize Repository (if not already done)
```bash
git init
git add .
git commit -m "Initial commit"
```

## Version Management Commands

### 1. Check Current Status
```bash
git status
```
**Screenshot:** Terminal showing git status

### 2. View Commit History
```bash
git log --oneline --graph --all
```
**Screenshot:** Terminal showing commit history

### 3. View Branches
```bash
git branch -a
```
**Screenshot:** Terminal showing branches

### 4. Create Version Tag
```bash
# Create version tag
git tag -a v1.0.0 -m "Version 1.0.0 - Initial release"
git tag -a v1.1.0 -m "Version 1.1.0 - Added AI features"
git tag -a v1.2.0 -m "Version 1.2.0 - Added quiz mode"

# View tags
git tag -l
```
**Screenshot:** Terminal showing version tags

### 5. View Tag Details
```bash
git show v1.0.0
```
**Screenshot:** Terminal showing tag details

### 6. Create Release Branch
```bash
git checkout -b release/v1.0.0
git checkout main
```
**Screenshot:** Terminal showing branch creation

### 7. View Differences Between Versions
```bash
git diff v1.0.0 v1.1.0
```
**Screenshot:** Terminal showing version differences

## Semantic Versioning

Follow semantic versioning: MAJOR.MINOR.PATCH

- **MAJOR**: Breaking changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes

## Version Screenshots Checklist

- [ ] Git status showing clean working directory
- [ ] Commit history with meaningful messages
- [ ] Version tags (v1.0.0, v1.1.0, etc.)
- [ ] Branch structure
- [ ] Version comparison (git diff)
- [ ] Release notes or CHANGELOG.md

## Create CHANGELOG.md

```bash
cat > CHANGELOG.md << 'EOF'
# Changelog

## [1.2.0] - 2025-11-07
### Added
- Quiz mode feature
- Integration with Gemini AI
- Flashcard generation

## [1.1.0] - 2025-11-07
### Added
- AI summarization
- Document upload
- User authentication

## [1.0.0] - 2025-11-07
### Added
- Initial release
- Basic Flask API
- User registration and login
EOF
```

**Screenshot:** CHANGELOG.md file

