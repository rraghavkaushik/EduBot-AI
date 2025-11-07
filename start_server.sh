#!/bin/bash
# EduBot Server Startup Script with Gemini API Key

export GEMINI_API_KEY="AIzaSyAN8Hfz6TYALvH2Jp-R3aIG7Bp-ST6tcno"

# Activate virtual environment
source venv/bin/activate

# Start Flask server
python app.py

