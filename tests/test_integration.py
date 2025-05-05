"""
Integration tests for the Memory Optimizer CLI tool.
"""

import unittest
import tempfile
import shutil
from pathlib import Path
import subprocess
import sys

class TestCLIIntegration(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.test_file = Path(self.temp_dir) / "test.py"
        
        # Create a test file with optimization opportunities
        self.test_file.write_text('''
def read_large_file(filename):
    with open(filename, 'r') as f:
        data = f.read()
    return [line.upper() for line in data.splitlines()]

class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
        ''')
        
    def tearDown(self):
        shutil.rmtree(self.temp_dir)
        
    def test_cli_optimize_file(self):
        """Test CLI file optimization."""
        # Run CLI command
        result = subprocess.run([
            sys.executable, '-m', 'memory_optimizer.cli',
            str(self.test_file),
            '--dry-run'
        ], capture_output=True, text=True)
        
        # Check command succeeded
        self.assertEqual(result.returncode, 0)
        self.assertIn('Files optimized: 1', result.stdout)
        
    def test_cli_optimize_directory(self):
        """Test CLI directory optimization."""
        # Create another test file
        another_file = Path(self.temp_dir) / "another.py"
        another_file.write_text('def test(): return [x for x in range(1000)]')
        
        # Run CLI command
        result = subprocess.run([
            sys.executable, '-m', 'memory_optimizer.cli',
            str(self.temp_dir),
            '--dry-run'
        ], capture_output=True, text=True)
        
        # Check command succeeded
        self.assertEqual(result.returncode, 0)
        self.assertIn('Total files processed: 2', result.stdout)
        
    def test_cli_with_tests(self):
        """Test CLI with test generation."""
        # Run CLI command with test generation
        result = subprocess.run([
            sys.executable, '-m', 'memory_optimizer.cli',
            str(self.test_file),
            '--dry-run',
            '--run-tests'
        ], capture_output=True, text=True)
        
        # Check command succeeded
        self.assertEqual(result.returncode, 0)
        self.assertIn('Running tests', result.stdout)