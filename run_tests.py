"""
run_tests.py  –  Bootstrap pytest and run the test suite.
Usage:  python run_tests.py        (from inside the venv)
"""
import subprocess
import sys
import os

base = os.path.dirname(os.path.abspath(__file__))
python = sys.executable

# 1. Ensure pytest is installed
subprocess.check_call([python, "-m", "pip", "install", "pytest", "--quiet"])

# 2. Run tests
result = subprocess.run(
    [python, "-m", "pytest", "tests/", "-v", "--tb=short"],
    cwd=base,
)
sys.exit(result.returncode)
