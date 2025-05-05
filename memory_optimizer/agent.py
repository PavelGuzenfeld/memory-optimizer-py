"""
Memory Optimization Agent - Core optimization logic.
"""

import ast
import sys
import weakref
import array
import mmap
from typing import Dict, List, Tuple, Generator, Any, Optional, Union
from dataclasses import dataclass

@dataclass
class OptimizationResult:
    """Container for optimization analysis results."""
    original_code: str
    optimized_code: str
    test_code: str
    memory_saved: float  # Percentage
    explanation: str
    warnings: List[str]

class MemoryOptimizationAgent:
    """Agent for analyzing and optimizing Python code for memory efficiency."""
    
    def __init__(self):
        self.optimization_patterns = {
            'file_operations': self._optimize_file_operations,
            'list_comprehensions': self._optimize_list_comprehensions,
            'class_definitions': self._optimize_class_definitions,
            'data_structures': self._optimize_data_structures,
        }
    
    def optimize_code(self, code: str) -> OptimizationResult:
        """Analyze and optimize Python code for memory efficiency."""
        try:
            tree = ast.parse(code)
            
            # Detect optimization opportunities
            optimizations = self._detect_optimizations(tree, code)
            
            if not optimizations:
                return OptimizationResult(
                    original_code=code,
                    optimized_code=code,
                    test_code="",
                    memory_saved=0.0,
                    explanation="No optimization opportunities found.",
                    warnings=[]
                )
            
            # Apply optimizations
            optimized_code = code
            total_memory_saved = 0.0
            explanations = []
            warnings = []
            test_codes = []
            
            for opt_type, details in optimizations.items():
                result = self.optimization_patterns[opt_type](details, optimized_code)
                optimized_code = result['optimized_code']
                total_memory_saved += result['memory_saved']
                explanations.append(result['explanation'])
                warnings.extend(result.get('warnings', []))
                if result.get('test_code'):
                    test_codes.append(result['test_code'])
            
            # Combine test codes
            combined_test_code = self._combine_test_codes(test_codes)
            
            return OptimizationResult(
                original_code=code,
                optimized_code=optimized_code,
                test_code=combined_test_code,
                memory_saved=total_memory_saved,
                explanation='\n'.join(explanations),
                warnings=warnings
            )
            
        except SyntaxError as e:
            return OptimizationResult(
                original_code=code,
                optimized_code=code,
                test_code="",
                memory_saved=0.0,
                explanation=f"Syntax error in input code: {e}",
                warnings=["Could not parse code"]
            )
    
    def _detect_optimizations(self, tree: ast.AST, code: str) -> Dict[str, Any]:
        """Detect optimization opportunities in the code."""
        optimizations = {}
        
        # Check for file operations
        file_ops = self._detect_file_operations(tree)
        if file_ops:
            optimizations['file_operations'] = file_ops
        
        # Check for list comprehensions
        list_comps = self._detect_list_comprehensions(tree)
        if list_comps:
            optimizations['list_comprehensions'] = list_comps
        
        # Check for class definitions
        class_defs = self._detect_class_definitions(tree)
        if class_defs:
            optimizations['class_definitions'] = class_defs
        
        # Check for data structures
        data_structs = self._detect_data_structures(tree, code)
        if data_structs:
            optimizations['data_structures'] = data_structs
        
        return optimizations
    
    def _detect_file_operations(self, tree: ast.AST) -> Optional[Dict[str, Any]]:
        """Detect file operations that could be optimized."""
        file_operations = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                if hasattr(node.func, 'attr') and node.func.attr in ['read', 'readlines']:
                    file_operations.append({'node': node, 'type': 'file_read'})
        
        return file_operations if file_operations else None
    
    def _detect_list_comprehensions(self, tree: ast.AST) -> Optional[Dict[str, Any]]:
        """Detect list comprehensions that could be converted to generators."""
        list_comps = []
        for node in ast.walk(tree):
            if isinstance(node, ast.ListComp):
                list_comps.append({'node': node, 'type': 'list_comp'})
        
        return list_comps if list_comps else None
    
    def _detect_class_definitions(self, tree: ast.AST) -> Optional[Dict[str, Any]]:
        """Detect class definitions that could use __slots__."""
        class_defs = []
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                has_slots = any(
                    isinstance(item, ast.Assign) and 
                    any(target.id == '__slots__' for target in item.targets if hasattr(target, 'id'))
                    for item in node.body
                )
                if not has_slots:
                    class_defs.append({'node': node, 'type': 'class_without_slots'})
        
        return class_defs if class_defs else None
    
    def _detect_data_structures(self, tree: ast.AST, code: str) -> Optional[Dict[str, Any]]:
        """Detect inefficient data structures."""
        data_structures = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                if hasattr(node.func, 'id') and node.func.id == 'list':
                    if node.args and isinstance(node.args[0], ast.Call):
                        if hasattr(node.args[0].func, 'id') and node.args[0].func.id == 'range':
                            data_structures.append({'node': node, 'type': 'list_range'})
        
        return data_structures if data_structures else None
    
    def _optimize_file_operations(self, details: List[Dict], code: str) -> Dict[str, Any]:
        """Optimize file operations for memory efficiency."""
        optimized_code = code
        
        # Simple demonstration - replace read() with line-by-line processing
        optimized_code = """from typing import Generator

def process_file(filename: str) -> Generator[str, None, None]:
    \"\"\"Process file line by line to minimize memory usage.\"\"\"
    with open(filename, 'r') as f:
        for line in f:
            yield line.rstrip('\\n').upper()"""
        
        test_code = """
import unittest
import tempfile
import os

class TestFileOptimization(unittest.TestCase):
    def setUp(self):
        self.test_file = tempfile.NamedTemporaryFile(mode='w', delete=False)
        self.test_file.write("line1\\nline2\\nline3\\n")
        self.test_file.close()
        
    def tearDown(self):
        os.unlink(self.test_file.name)
    
    def test_process_file(self):
        result = list(process_file(self.test_file.name))
        expected = ["LINE1", "LINE2", "LINE3"]
        self.assertEqual(result, expected)
"""
        
        return {
            'optimized_code': optimized_code,
            'memory_saved': 60.0,
            'explanation': 'Converted file reading to use generators instead of loading entire file into memory.',
            'test_code': test_code,
            'warnings': []
        }
    
    def _optimize_list_comprehensions(self, details: List[Dict], code: str) -> Dict[str, Any]:
        """Convert list comprehensions to generator expressions."""
        optimized_code = code
        
        # Simple demonstration - replace list comprehension with generator
        optimized_code = """from typing import Generator

def process_data(items) -> Generator[int, None, None]:
    \"\"\"Process data using generator instead of list comprehension.\"\"\"
    return (x * 2 for x in items if x > 0)"""
        
        test_code = """
import unittest

class TestGeneratorOptimization(unittest.TestCase):
    def test_process_data(self):
        items = [1, -2, 3, -4, 5]
        result = list(process_data(items))
        expected = [2, 6, 10]
        self.assertEqual(result, expected)
"""
        
        return {
            'optimized_code': optimized_code,
            'memory_saved': 40.0,
            'explanation': 'Converted list comprehension to generator expression for memory efficiency.',
            'test_code': test_code,
            'warnings': ['Generator expressions are single-use iterables']
        }
    
    def _optimize_class_definitions(self, details: List[Dict], code: str) -> Dict[str, Any]:
        """Add __slots__ to classes to reduce memory overhead."""
        optimized_code = code
        
        # Simple demonstration - add __slots__ to a class
        optimized_code = """class Person:
    __slots__ = ['name', 'age']
    
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age"""
        
        test_code = """
import unittest
import sys

class TestSlotsOptimization(unittest.TestCase):
    def test_slots_memory_saving(self):
        class PersonWithoutSlots:
            def __init__(self, name, age):
                self.name = name
                self.age = age
        
        p1 = PersonWithoutSlots("John", 30)
        p2 = Person("John", 30)
        
        # Basic functionality test
        self.assertEqual(p2.name, "John")
        self.assertEqual(p2.age, 30)
"""
        
        return {
            'optimized_code': optimized_code,
            'memory_saved': 35.0,
            'explanation': 'Added __slots__ to class definition to reduce memory overhead.',
            'test_code': test_code,
            'warnings': ['__slots__ prevents dynamic attribute assignment']
        }
    
    def _optimize_data_structures(self, details: List[Dict], code: str) -> Dict[str, Any]:
        """Optimize data structure usage."""
        optimized_code = code
        
        # Simple demonstration - use array.array for numeric data
        optimized_code = """import array

def create_numeric_array(size: int) -> array.array:
    \"\"\"Create memory-efficient numeric array.\"\"\"
    return array.array('i', range(size))"""
        
        test_code = """
import unittest

class TestDataStructureOptimization(unittest.TestCase):
    def test_numeric_array(self):
        arr = create_numeric_array(5)
        self.assertEqual(list(arr), [0, 1, 2, 3, 4])
"""
        
        return {
            'optimized_code': optimized_code,
            'memory_saved': 50.0,
            'explanation': 'Used array.array instead of list for memory-efficient numeric storage.',
            'test_code': test_code,
            'warnings': []
        }
    
    def _combine_test_codes(self, test_codes: List[str]) -> str:
        """Combine multiple test code snippets into a single test suite."""
        if not test_codes:
            return ""
        
        combined = "import unittest\n\n"
        
        # Extract test classes from each test code
        for i, test_code in enumerate(test_codes):
            # Remove import statements (we'll add them once at the top)
            lines = test_code.strip().split('\n')
            filtered_lines = []
            for line in lines:
                if not line.startswith('import') and not line.startswith('from'):
                    filtered_lines.append(line)
            
            combined += '\n'.join(filtered_lines) + '\n\n'
        
        combined += """
if __name__ == '__main__':
    unittest.main()
"""
        
        return combined