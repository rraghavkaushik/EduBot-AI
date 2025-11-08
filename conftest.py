"""
Pytest configuration for mutation testing.
This file ensures that imports work correctly when tests run from the mutants directory.
"""
import sys
import os

# Add parent directory to Python path so imports work from mutants directory
parent_dir = os.path.dirname(os.path.abspath(__file__))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

