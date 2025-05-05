"""
Optimization strategies for the Memory Optimizer tool.
"""

import ast
import re
from typing import Dict, List, Any, Optional

class MemoryOptimizer:
    """Applies memory optimization strategies to Python code."""
    
    def __init__(self):
        self.strategies = {
            'generator_conversion': self._apply_generator_conversion,
            'slots_addition': self._add_slots_to_classes,
            'memory_mapping': self._apply_memory_mapping,
            'object_pooling': self._implement_object_pooling,
        }
    
    def apply_optimization(self, code: str, strategy: str) -> Dict[str, Any]:
        """Apply a specific optimization strategy to the code."""
        if strategy not in self.strategies:
            raise ValueError(f"Unknown optimization strategy: {strategy}")
        
        return self.strategies[strategy](code)
    
    def _apply_generator_conversion(self, code: str) -> Dict[str, Any]:
        """Convert list comprehensions to generator expressions."""
        try:
            tree = ast.parse(code)
            
            # Check if there are list comprehensions to convert
            list_comp_found = False
            for node in ast.walk(tree):
                if isinstance(node, ast.ListComp):
                    list_comp_found = True
                    break
            
            if not list_comp_found:
                # No list comprehensions found, return unchanged
                return {
                    'success': False,  # Fixed: Return success=False when no changes
                    'optimized_code': code,
                    'changes': []
                }
            
            # Convert list comprehensions to generator expressions
            # For Python 3.8 compatibility, use regex-based approach instead of ast.unparse
            if ('[' in code) and ('for' in code) and ('in' in code):
                optimized_code = re.sub(
                    r'\[(.*?) for (.*?) in (.*?)( if (.*?))?\]',
                    r'(\1 for \2 in \3\4)',
                    code
                )
                
                return {
                    'success': True,
                    'optimized_code': optimized_code,
                    'changes': ['Converted list comprehensions to generator expressions']
                }
            
            return {
                'success': False,  # Fixed: Return success=False when no changes
                'optimized_code': code,
                'changes': []
            }
            
        except Exception as e:
            return {
                'success': False,
                'optimized_code': code,
                'error': str(e)
            }
    
    def _add_slots_to_classes(self, code: str) -> Dict[str, Any]:
        """Add __slots__ to class definitions."""
        try:
            tree = ast.parse(code)
            
            # Check if there are classes to modify
            class_found = False
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    class_found = True
                    break
            
            if not class_found:
                # No classes found, return unchanged
                return {
                    'success': False,  # Fixed: Return success=False when no changes
                    'optimized_code': code,
                    'changes': []
                }
            
            # Extract instance variables and class names
            class_info = {}
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    class_name = node.name
                    instance_vars = []
                    
                    # Check if class already has __slots__
                    has_slots = any(
                        isinstance(item, ast.Assign) and
                        any(target.id == '__slots__' for target in item.targets if hasattr(target, 'id'))
                        for item in node.body
                    )
                    
                    if not has_slots:
                        # Extract instance variables from __init__
                        for item in node.body:
                            if isinstance(item, ast.FunctionDef) and item.name == '__init__':
                                for stmt in ast.walk(item):
                                    if isinstance(stmt, ast.Assign):
                                        for target in stmt.targets:
                                            if (isinstance(target, ast.Attribute) and
                                                isinstance(target.value, ast.Name) and
                                                target.value.id == 'self'):
                                                instance_vars.append(target.attr)
                        
                        if instance_vars:
                            class_info[class_name] = instance_vars
            
            # If no classes need slots, return unchanged
            if not class_info:
                return {
                    'success': False,  # Fixed: Return success=False when no changes
                    'optimized_code': code,
                    'changes': []
                }
            
            # Add __slots__ to each class
            optimized_code = code
            for class_name, instance_vars in class_info.items():
                slots_list = ", ".join([f"'{var}'" for var in instance_vars])
                pattern = rf'class {class_name}[^:]*:'
                replacement = f'class {class_name}:\n    __slots__ = [{slots_list}]'
                optimized_code = re.sub(pattern, replacement, optimized_code)
            
            return {
                'success': True,
                'optimized_code': optimized_code,
                'changes': ['Added __slots__ to class definitions']
            }
            
        except Exception as e:
            return {
                'success': False,
                'optimized_code': code,
                'error': str(e)
            }
    
    def _apply_memory_mapping(self, code: str) -> Dict[str, Any]:
        """Apply memory mapping for file operations."""
        # Detect file.read() patterns
        pattern = r'with\s+open\([^)]+\)\s+as\s+(\w+):\s*\n\s*(\w+)\s*=\s*\1\.read\(\)'
        
        if re.search(pattern, code):
            # Replace with mmap pattern
            replacement = """import mmap

def read_large_file(filename):
    \"\"\"Read file using memory-mapped file for efficiency.\"\"\"
    with open(filename, 'rb') as f:
        with mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ) as mm:
            # Process the memory-mapped file
            return mm.read().decode('utf-8')"""
            
            return {
                'success': True,
                'optimized_code': replacement,
                'changes': ['Applied memory mapping for file operations']
            }
        
        return {
            'success': False,  # Fixed: Return success=False when no changes
            'optimized_code': code,
            'changes': []
        }
    
    def _implement_object_pooling(self, code: str) -> Dict[str, Any]:
        """Implement object pooling for frequently created objects."""
        # Detect repeated object creation
        pattern = r'for\s+.*\s+in\s+.*:\s*\n\s*.*=\s*\w+\([^)]*\)'
        
        if re.search(pattern, code):
            # Add object pooling
            pool_template = """
# Add object pooling for better memory efficiency
class ObjectPool:
    def __init__(self, factory, max_size=100):
        self.factory = factory
        self.pool = []
        self.max_size = max_size
    
    def acquire(self):
        if self.pool:
            return self.pool.pop()
        return self.factory()
    
    def release(self, obj):
        if len(self.pool) < self.max_size:
            self.pool.append(obj)

# Example usage:
# pool = ObjectPool(lambda: ExpensiveObject())
# obj = pool.acquire()
# # Use obj...
# pool.release(obj)
"""
            
            return {
                'success': True,
                'optimized_code': code + pool_template,
                'changes': ['Added object pooling implementation']
            }
        
        return {
            'success': False,  # Fixed: Return success=False when no changes
            'optimized_code': code,
            'changes': []
        }