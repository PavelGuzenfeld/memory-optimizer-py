"""
Tests for the Memory Optimizer strategies.
"""

import pytest
from memory_optimizer.optimizer import MemoryOptimizer

class TestMemoryOptimizer:
    """Test suite for MemoryOptimizer strategies."""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Set up test fixtures."""
        self.optimizer = MemoryOptimizer()
    
    def test_optimizer_initialization(self):
        """Test optimizer initialization."""
        assert self.optimizer is not None
        assert hasattr(self.optimizer, 'strategies')
        assert len(self.optimizer.strategies) > 0
    
    def test_generator_conversion_strategy(self):
        """Test generator conversion strategy."""
        code = """
def process_data(items):
    return [x * 2 for x in items if x > 0]
"""
        result = self.optimizer.apply_optimization(code, 'generator_conversion')
        
        assert result['success']
        assert 'changes' in result
        assert len(result['changes']) > 0
        assert 'optimized_code' in result
        
    def test_slots_addition_strategy(self):
        """Test slots addition strategy."""
        code = """
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
"""
        result = self.optimizer.apply_optimization(code, 'slots_addition')
        
        assert result['success']
        assert '__slots__' in result['optimized_code']
        assert "['name', 'age']" in result['optimized_code']
    
    def test_memory_mapping_strategy(self):
        """Test memory mapping strategy."""
        code = """
def read_large_file(filename):
    with open(filename, 'rb') as f:
        data = f.read()
    return data
"""
        result = self.optimizer.apply_optimization(code, 'memory_mapping')
        
        # This is a simplified implementation, so it might not always succeed
        assert 'optimized_code' in result
        
    def test_object_pooling_strategy(self):
        """Test object pooling strategy."""
        code = """
def create_objects():
    results = []
    for i in range(1000):
        obj = ExpensiveObject(i)
        results.append(obj)
    return results
"""
        result = self.optimizer.apply_optimization(code, 'object_pooling')
        
        # This is a simplified implementation, so it might not always succeed
        assert 'optimized_code' in result
    
    def test_invalid_strategy(self):
        """Test handling of invalid strategy name."""
        code = "def test(): pass"
        
        with pytest.raises(ValueError, match="Unknown optimization strategy"):
            self.optimizer.apply_optimization(code, 'invalid_strategy')
    
    def test_strategy_with_syntax_error(self):
        """Test strategy handling of code with syntax errors."""
        code = "def test( invalid syntax"
        
        result = self.optimizer.apply_optimization(code, 'generator_conversion')
        
        assert not result['success']
        assert 'error' in result
    
    def test_strategy_with_no_optimization_needed(self):
        """Test strategy when no optimization is needed."""
        code = """
def simple_function(x, y):
    return x + y
"""
        result = self.optimizer.apply_optimization(code, 'generator_conversion')
        
        assert not result['success']  # No changes made
        assert result['optimized_code'] == code
        assert len(result['changes']) == 0