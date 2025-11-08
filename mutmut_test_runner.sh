#!/bin/bash
# Wrapper script for mutmut to run tests with proper dependencies

BASE_DIR="/Users/rraghavkaushik/Documents/SEM-7/SWE/EduBot"
MUTANTS_DIR="$BASE_DIR/mutants"

# Copy dependencies to mutants directory
if [ -d "$BASE_DIR/services" ] && [ ! -d "$MUTANTS_DIR/services" ]; then
    cp -r "$BASE_DIR/services" "$MUTANTS_DIR/"
fi

if [ -f "$BASE_DIR/gemini_service.py" ] && [ ! -f "$MUTANTS_DIR/gemini_service.py" ]; then
    cp "$BASE_DIR/gemini_service.py" "$MUTANTS_DIR/"
fi

if [ -f "$BASE_DIR/text_extractor.py" ] && [ ! -f "$MUTANTS_DIR/text_extractor.py" ]; then
    cp "$BASE_DIR/text_extractor.py" "$MUTANTS_DIR/"
fi

# Run pytest from mutants directory with parent in PYTHONPATH
cd "$MUTANTS_DIR"
export PYTHONPATH="$BASE_DIR:$PYTHONPATH"
pytest "$@"

