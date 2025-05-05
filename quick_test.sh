#!/bin/bash
# quick_test.sh - Quick test runner for development

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${GREEN}Running Memory Optimizer Tests...${NC}"
echo "================================"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}Virtual environment not found. Creating with Python 3.8...${NC}"
    python3.8 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Make sure pip and setuptools are up to date in venv
python -m pip install --upgrade pip setuptools wheel

# Install dependencies
echo -e "${YELLOW}Installing dependencies...${NC}"
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Set PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# Run tests
echo -e "\n${GREEN}Running unit tests...${NC}"
python -m pytest tests/ -v --cov=memory_optimizer

# Check exit code
if [ $? -eq 0 ]; then
    echo -e "\n${GREEN}All tests passed!${NC}"
else
    echo -e "\n${RED}Tests failed!${NC}"
    exit 1
fi

# Run linting
echo -e "\n${GREEN}Running linting...${NC}"
python -m flake8 memory_optimizer tests || exit 1

# Run type checking
echo -e "\n${GREEN}Running type checking...${NC}"
python -m mypy memory_optimizer || exit 1

echo -e "\n${GREEN}All checks passed!${NC}"
