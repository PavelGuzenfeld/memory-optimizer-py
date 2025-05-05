#!/bin/bash
# quick_test.sh - Quick test runner for development

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}Running Memory Optimizer Tests...${NC}"
echo "================================"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}Virtual environment not found. Creating...${NC}"
    python3.8 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Check if dependencies are installed
if ! python -c "import pytest" 2>/dev/null; then
    echo -e "${YELLOW}Installing dependencies...${NC}"
    pip install -r requirements.txt
    pip install -r requirements-dev.txt
fi

# Set PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# Run tests
echo -e "\n${GREEN}Running unit tests...${NC}"
pytest tests/ -v --cov=memory_optimizer

# Check exit code
if [ $? -eq 0 ]; then
    echo -e "\n${GREEN}All tests passed!${NC}"
else
    echo -e "\n${RED}Tests failed!${NC}"
    exit 1
fi

# Run linting
echo -e "\n${GREEN}Running linting...${NC}"
flake8 memory_optimizer tests || exit 1

# Run type checking
echo -e "\n${GREEN}Running type checking...${NC}"
mypy memory_optimizer || exit 1

echo -e "\n${GREEN}All checks passed!${NC}"
