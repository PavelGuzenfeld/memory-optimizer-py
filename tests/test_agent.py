"""
Tests for the Memory Optimization Agent.
"""

import unittest
import tempfile
import os
from pathlib import Path

from memory_optimizer.agent import MemoryOptimizationAgent
from memory_optimizer.analyzer import CodeAnalyzer

class TestMemoryOptimizationAgent(unittest.TestCase):
    def setUp(self):
        self.agent = MemoryOptimizationAgent()
        self.analyzer = CodeAnalyzer()
        
    def test_optimize_file_operations(self):
        """Test optimization of file operations."""
        code = '''
def read_file(filename):
    with open(filename, 'r') as f:
        data = f.read()
    return [line.upper() for line in data.splitlines()]
        '''
        
        result = self.agent.optimize_code(code)
        
        # Check that optimization was made
        self.assertGreater(result.memory_saved, 0)
        self.assertIn('Generator', result.optimized_code)
        self.assertIn('yield', result.optimized_code)
        
    def test_optimize_list_comprehension(self):
        """Test optimization of list comprehensions."""
        code = '''
def process_data(items):
    return [x * 2 for x in items if x > 0]
        '''
        
        result = self.agent.optimize_code(code)
        
        # Check that generator is used
        self.assertGreater(result.memory_saved, 0)
        self.assertIn('Generator', result.optimized_code)
        
    def test_optimize_class_with_slots(self):
        """Test optimization of classes using __slots__."""
        code = '''
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
        '''
        
        result = self.agent.optimize_code(code)
        
        # Check that __slots__ is added
        self.assertGreater(result.memory_saved, 0)
        self.assertIn('__slots__', result.optimized_code)
        
    def test_no_optimization_needed(self):
        """Test when no optimization is needed."""
        code = '''
def simple_function(x, y):
    return x + y
        '''
        
        result = self.agent.optimize_code(code)
        
        # Check that no changes were made
        self.assertEqual(result.memory_saved, 0)
        self.assertEqual(result.optimized_code, code)