# Makefile for memory_optimizer

.PHONY: test clean install dev-install lint type-check coverage format docs

# Variables
PYTHON := python3.8
VENV := venv
BIN := $(VENV)/bin

# Default target
all: test

# Create virtual environment
venv:
	$(PYTHON) -m venv $(VENV)
	$(BIN)/pip install --upgrade pip

# Install package in development mode
dev-install: venv
	$(BIN)/pip install -e .
	$(BIN)/pip install -r requirements-dev.txt

# Install package normally
install: venv
	$(BIN)/pip install .

# Run all tests
test:
	$(BIN)/pytest tests/ -v

# Run tests with coverage
coverage:
	$(BIN)/pytest tests/ --cov=memory_optimizer --cov-report=html
	@echo "Coverage report generated in htmlcov/index.html"

# Run linting
lint:
	$(BIN)/flake8 memory_optimizer tests

# Run type checking
type-check:
	$(BIN)/mypy memory_optimizer

# Format code
format:
	$(BIN)/black memory_optimizer tests
	$(BIN)/isort memory_optimizer tests

# Run all checks
check: lint type-check test

# Build documentation
docs:
	cd docs && $(BIN)/sphinx-build -b html . _build/html

# Clean up generated files
clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf .mypy_cache/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.bak.py" -delete
	find . -type f -name ".coverage" -delete

# Create distribution packages
dist: clean
	$(BIN)/python setup.py sdist bdist_wheel

# Upload to PyPI
upload: dist
	$(BIN)/twine upload dist/*

# Help target
help:
	@echo "Available targets:"
	@echo "  make dev-install  - Install package in development mode"
	@echo "  make test         - Run all tests"
	@echo "  make coverage     - Run tests with coverage report"
	@echo "  make lint         - Run code linting"
	@echo "  make type-check   - Run type checking"
	@echo "  make format       - Format code with black and isort"
	@echo "  make check        - Run all checks (lint, type-check, test)"
	@echo "  make docs         - Build documentation"
	@echo "  make clean        - Clean up generated files"
	@echo "  make dist         - Create distribution packages"
	@echo "  make upload       - Upload to PyPI"
