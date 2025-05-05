# run_tests.py

```python
#!/usr/bin/env python3
"""
Test runner for the memory_optimizer package.
This allows testing without installation.
"""

import sys
import os
import unittest
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def run_all_tests():
    """Run all tests in the tests directory."""
    loader = unittest.TestLoader()
    start_dir = project_root / 'tests'
    suite = loader.discover(start_dir, pattern='test_*.py')
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()

def run_specific_test(test_name):
    """Run a specific test module, class, or method."""
    loader = unittest.TestLoader()
    
    try:
        if '.' in test_name:
            # Run specific test class or method
            suite = loader.loadTestsFromName(f'tests.{test_name}')
        else:
            # Run entire test module
            suite = loader.loadTestsFromName(f'tests.test_{test_name}')
        
        runner = unittest.TextTestRunner(verbosity=2)
        result = runner.run(suite)
        return result.wasSuccessful()