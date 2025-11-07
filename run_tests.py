#!/usr/bin/env python3
"""
Simple test runner for EduBot backend tests.
Run this script to execute all tests with coverage.
"""

import subprocess
import sys
import os

def run_tests():
    """Run the test suite with coverage."""
    print("🧪 Running EduBot Backend Tests...")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists('app.py'):
        print("❌ Error: app.py not found. Please run this from the EduBot root directory.")
        sys.exit(1)
    
    # Run tests with coverage
    try:
        result = subprocess.run([
            'python', '-m', 'pytest', 
            'test_app.py', 
            '-v', 
            '--cov=app',
            '--cov-report=term-missing',
            '--cov-report=html'
        ], capture_output=True, text=True)
        
        print(result.stdout)
        
        if result.stderr:
            print("Warnings/Errors:")
            print(result.stderr)
        
        if result.returncode == 0:
            print("\n✅ All tests passed!")
        else:
            print(f"\n❌ Tests failed with exit code {result.returncode}")
            
    except FileNotFoundError:
        print("❌ Error: pytest not found. Please install test dependencies:")
        print("   pip install -r test_requirements.txt")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error running tests: {e}")
        sys.exit(1)

if __name__ == '__main__':
    run_tests()


