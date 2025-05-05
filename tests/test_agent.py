# test_agent.py
"""
Comprehensive tests for the Memory Optimization Agent.
"""

import pytest
import tempfile
import os
from pathlib import Path
from typing import Dict, Any

from memory_optimizer.agent import MemoryOptimizationAgent, OptimizationResult
from tests.fixtures.sample_code import (
    FILE_OPERATION_CODE,
    CLASS_WITHOUT_SLOTS,
    LIST_COMPREHENSION_CODE,
    NESTED_COMPREHENSION_CODE,
    COMPLEX_CLASS_CODE,
    LARGE_DATA_STRUCTURE_CODE,
    FILE_WITH_READLINES,
    MULTIPLE_LIST_COMPREHENSIONS,
    MIXED_OPTIMIZATION_OPPORTUNITIES,
    ALREADY_OPTIMIZED_CODE,
    SYNTAX_ERROR_CODE,
    SIMPLE_FUNCTION_CODE
)

class TestMemoryOptimizationAgent:
    """Test suite for MemoryOptimizationAgent."""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Set up test fixtures."""
        self.agent = MemoryOptimizationAgent()
    
    # Basic functionality tests
    
    def test_agent_initialization(self):
        """Test agent initialization."""
        assert self.agent is not None
        assert hasattr(self.agent, 'optimize_code')
        assert hasattr(self.agent, 'optimization_patterns')
    
    # File operation tests
    
    def test_optimize_file_read_operations(self):
        """Test optimization of file read operations."""
        result = self.agent.optimize_code(FILE_OPERATION_CODE)
        
        assert result.memory_saved > 0
        assert 'Generator' in result.optimized_code
        assert 'yield' in result.optimized_code
        assert 'typing' in result.optimized_code
    
    def test_optimize_file_readlines_operations(self):
        """Test optimization of file readlines operations."""
        result = self.agent.optimize_code(FILE_WITH_READLINES)
        
        assert result.memory_saved > 0
        assert 'yield' in result.optimized_code
        assert 'for line in f:' in result.optimized_code
    
    # Class optimization tests
    
    def test_optimize_simple_class(self):
        """Test optimization of a simple class with __slots__."""
        result = self.agent.optimize_code(CLASS_WITHOUT_SLOTS)
        
        assert result.memory_saved > 0
        assert '__slots__' in result.optimized_code
        assert "['name', 'age'" in result.optimized_code
    
    def test_optimize_complex_class(self):
        """Test optimization of a complex class with multiple attributes."""
        result = self.agent.optimize_code(COMPLEX_CLASS_CODE)
        
        assert result.memory_saved > 0
        assert '__slots__' in result.optimized_code
        assert all(attr in result.optimized_code for attr in ['name', 'age', 'email', 'address'])
    
    def test_class_already_optimized(self):
        """Test that already optimized classes are not modified."""
        result = self.agent.optimize_code(ALREADY_OPTIMIZED_CODE)
        
        assert result.memory_saved == 0
        assert result.optimized_code == ALREADY_OPTIMIZED_CODE
    
    # List comprehension tests
    
    def test_optimize_simple_list_comprehension(self):
        """Test optimization of simple list comprehensions."""
        result = self.agent.optimize_code(LIST_COMPREHENSION_CODE)
        
        assert result.memory_saved > 0
        assert 'Generator' in result.optimized_code
        assert 'n * 2 for n in numbers if n > 0' in result.optimized_code
    
    def test_optimize_nested_list_comprehension(self):
        """Test optimization of nested list comprehensions."""
        result = self.agent.optimize_code(NESTED_COMPREHENSION_CODE)
        
        assert result.memory_saved > 0
        assert 'Generator' in result.optimized_code
    
    def test_optimize_multiple_list_comprehensions(self):
        """Test optimization of multiple list comprehensions."""
        result = self.agent.optimize_code(MULTIPLE_LIST_COMPREHENSIONS)
        
        assert result.memory_saved > 0
        assert 'Generator' in result.optimized_code
        assert result.optimized_code.count('for') >= MULTIPLE_LIST_COMPREHENSIONS.count('for')
    
    # Data structure tests
    
    def test_optimize_large_data_structures(self):
        """Test optimization of large data structures."""
        result = self.agent.optimize_code(LARGE_DATA_STRUCTURE_CODE)
        
        assert result.memory_saved > 0
        assert any(opt in result.optimized_code for opt in ['array.array', 'Generator', 'numpy'])
    
    # Edge cases and error handling
    
    def test_invalid_syntax(self):
        """Test handling of invalid Python syntax."""
        result = self.agent.optimize_code(SYNTAX_ERROR_CODE)
        
        assert result.memory_saved == 0
        assert 'Syntax error' in result.explanation
        assert result.warnings
    
    def test_empty_code(self):
        """Test handling of empty code."""
        result = self.agent.optimize_code('')
        
        assert result.memory_saved == 0
        assert result.optimized_code == ''
    
    def test_non_optimizable_code(self):
        """Test code that doesn't need optimization."""
        result = self.agent.optimize_code(SIMPLE_FUNCTION_CODE)
        
        assert result.memory_saved == 0
        assert result.optimized_code == SIMPLE_FUNCTION_CODE
    
    # Integration tests
    
    def test_multiple_optimizations(self):
        """Test multiple optimizations in one code block."""
        result = self.agent.optimize_code(MIXED_OPTIMIZATION_OPPORTUNITIES)
        
        assert result.memory_saved > 30  # Expect significant savings
        assert '__slots__' in result.optimized_code
        assert 'yield' in result.optimized_code
        assert 'Generator' in result.optimized_code
    
    # Test generation verification
    
    def test_test_code_generation(self):
        """Test that test code is generated for optimizations."""
        result = self.agent.optimize_code(FILE_OPERATION_CODE)
        
        assert result.test_code
        assert 'unittest' in result.test_code
        assert 'test_' in result.test_code
        assert 'assertEqual' in result.test_code
    
    def test_test_code_validity(self):
        """Test that generated test code is valid Python."""
        result = self.agent.optimize_code(CLASS_WITHOUT_SLOTS)
        
        if result.test_code:
            try:
                compile(result.test_code, '<string>', 'exec')
                assert True
            except SyntaxError:
                pytest.fail("Generated test code has syntax errors")
    
    # Result structure tests
    
    def test_optimization_result_structure(self):
        """Test the structure of OptimizationResult."""
        result = self.agent.optimize_code(FILE_OPERATION_CODE)
        
        assert isinstance(result, OptimizationResult)
        assert hasattr(result, 'original_code')
        assert hasattr(result, 'optimized_code')
        assert hasattr(result, 'test_code')
        assert hasattr(result, 'memory_saved')
        assert hasattr(result, 'explanation')
        assert hasattr(result, 'warnings')
    
    # Performance tests
    
    @pytest.mark.performance
    def test_large_code_optimization(self):
        """Test optimization performance on large code."""
        # Generate large code sample
        large_code = '\n'.join([
            f'''
def process_file_{i}(filename):
    with open(filename, 'r') as f:
        data = f.read()
    return [line.upper() for line in data.splitlines()]
            ''' for i in range(100)
        ])
        
        import time
        start_time = time.time()
        result = self.agent.optimize_code(large_code)
        execution_time = time.time() - start_time
        
        assert execution_time < 5.0  # Should complete within 5 seconds
        assert result.memory_saved > 0
    
    @pytest.mark.memory
    def test_agent_memory_usage(self):
        """Test agent's own memory usage."""
        import tracemalloc
        
        tracemalloc.start()
        
        # Perform multiple optimizations
        for _ in range(10):
            self.agent.optimize_code(FILE_OPERATION_CODE)
        
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        
        assert peak < 50 * 1024 * 1024  # Less than 50MB
    
    # Specific optimization pattern tests
    
    def test_generator_conversion(self):
        """Test conversion of list comprehensions to generators."""
        code = "result = [x * 2 for x in range(100)]"
        result = self.agent.optimize_code(code)
        
        assert 'Generator' in result.optimized_code or '(' in result.optimized_code
    
    def test_slots_addition(self):
        """Test addition of __slots__ to classes."""
        code = """
class Example:
    def __init__(self, value):
        self.value = value
        """
        result = self.agent.optimize_code(code)
        
        assert '__slots__' in result.optimized_code
    
    def test_type_hints_addition(self):
        """Test that type hints are added to optimized code."""
        result = self.agent.optimize_code(FILE_OPERATION_CODE)
        
        assert ':' in result.optimized_code  # Type hints use colons
        assert any(t in result.optimized_code for t in ['str', 'int', 'Generator'])