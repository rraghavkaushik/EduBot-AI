#!/bin/bash
# EduBot Server Startup Script with Gemini API Key

export GEMINI_API_KEY=""

# Activate virtual environment
source venv/bin/activate

# Start Flask server
python app.py

