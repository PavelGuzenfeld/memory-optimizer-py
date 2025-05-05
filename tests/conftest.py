# tests/conftest.py

"""
Pytest configuration and fixtures for testing.
"""

import pytest
import tempfile
import shutil
from pathlib import Path

@pytest.fixture
def temp_dir():
    """Create a temporary directory for testing."""
    temp_dir = tempfile.mkdtemp()
    yield Path(temp_dir)
    shutil.rmtree(temp_dir)

@pytest.fixture
def sample_python_file(temp_dir):
    """Create a sample Python file with optimization opportunities."""
    file_path = temp_dir / "sample.py"
    file_path.write_text('''
def read_large_file(filename):
    with open(filename, 'r') as f:
        data = f.read()
    return [line.upper() for line in data.splitlines()]

class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

def process_data(items):
    return [x * 2 for x in items if x > 0]
''')
    return file_path

@pytest.fixture
def sample_test_data(temp_dir):
    """Create sample test data files."""
    # Create a large text file
    large_file = temp_dir / "large_file.txt"
    with open(large_file, 'w') as f:
        for i in range(10000):
            f.write(f"Line {i}\\n")
    
    # Create a CSV file
    csv_file = temp_dir / "data.csv"
    with open(csv_file, 'w') as f:
        f.write("id,value\\n")
        for i in range(1000):
            f.write(f"{i},{i * 10}\\n")
    
    return {
        'large_file': large_file,
        'csv_file': csv_file
    }

@pytest.fixture
def mock_agent():
    """Create a mock MemoryOptimizationAgent for testing."""
    from memory_optimizer.agent import MemoryOptimizationAgent
    return MemoryOptimizationAgent()

@pytest.fixture
def mock_analyzer():
    """Create a mock CodeAnalyzer for testing."""
    from memory_optimizer.analyzer import CodeAnalyzer
    return CodeAnalyzer()

@pytest.fixture
def test_project_dir(temp_dir):
    """Create a test project directory with multiple Python files."""
    project_dir = temp_dir / "test_project"
    project_dir.mkdir()
    
    # Create main.py
    main_file = project_dir / "main.py"
    main_file.write_text('''
def main():
    with open("data.txt", "r") as f:
        data = f.read()
    
    results = [line.upper() for line in data.splitlines()]
    return results

class DataProcessor:
    def __init__(self, name):
        self.name = name
        self.cache = {}
''')
    
    # Create utils.py
    utils_file = project_dir / "utils.py"
    utils_file.write_text('''
def read_csv(filename):
    with open(filename, "r") as f:
        lines = f.readlines()
    return [line.split(",") for line in lines]

class Helper:
    def __init__(self, value):
        self.value = value
''')
    
    # Create data file
    data_file = project_dir / "data.txt"
    data_file.write_text("line1\\nline2\\nline3\\n")
    
    return project_dir

# Add markers for pytest
def pytest_configure(config):
    config.addinivalue_line(
        "markers", "performance: mark test as a performance test"
    )
    config.addinivalue_line(
        "markers", "memory: mark test as a memory usage test"
    )
    config.addinivalue_line(
        "markers", "integration: mark test as an integration test"
    )
    config.addinivalue_line(
        "markers", "slow: mark test as slow"
    )
```