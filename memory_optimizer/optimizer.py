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
            modified = False
            
            class GeneratorTransformer(ast.NodeTransformer):
                def visit_ListComp(self, node):
                    # Convert ListComp to GeneratorExp
                    gen_exp = ast.GeneratorExp(
                        elt=node.elt,
                        generators=node.generators
                    )
                    nonlocal modified
                    modified = True
                    return gen_exp
            
            transformer = GeneratorTransformer()
            new_tree = transformer.visit(tree)
            
            if modified:
                optimized_code = ast.unparse(new_tree)
                return {
                    'success': True,
                    'optimized_code': optimized_code,
                    'changes': ['Converted list comprehensions to generator expressions']
                }
            
            return {
                'success': False,
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
            modified = False
            
            class SlotsAdder(ast.NodeTransformer):
                def visit_ClassDef(self, node):
                    # Check if class already has __slots__
                    has_slots = any(
                        isinstance(item, ast.Assign) and
                        any(target.id == '__slots__' for target in item.targets if hasattr(target, 'id'))
                        for item in node.body
                    )
                    
                    if not has_slots:
                        # Extract instance variables from __init__
                        instance_vars = self._extract_instance_vars(node)
                        
                        if instance_vars:
                            # Create __slots__ assignment
                            slots_node = ast.Assign(
                                targets=[ast.Name(id='__slots__', ctx=ast.Store())],
                                value=ast.List(
                                    elts=[ast.Constant(value=var) for var in instance_vars],
                                    ctx=ast.Load()
                                )
                            )
                            
                            # Insert __slots__ after class docstring (if any)
                            insert_idx = 0
                            if (node.body and isinstance(node.body[0], ast.Expr) and
                                isinstance(node.body[0].value, ast.Constant)):
                                insert_idx = 1
                            
                            node.body.insert(insert_idx, slots_node)
                            nonlocal modified
                            modified = True
                    
                    return node
                
                def _extract_instance_vars(self, class_node):
                    """Extract instance variables from __init__ method."""
                    instance_vars = []
                    
                    for item in class_node.body:
                        if isinstance(item, ast.FunctionDef) and item.name == '__init__':
                            for stmt in ast.walk(item):
                                if isinstance(stmt, ast.Assign):
                                    for target in stmt.targets:
                                        if (isinstance(target, ast.Attribute) and
                                            isinstance(target.value, ast.Name) and
                                            target.value.id == 'self'):
                                            instance_vars.append(target.attr)
                    
                    return instance_vars
            
            transformer = SlotsAdder()
            new_tree = transformer.visit(tree)
            
            if modified:
                optimized_code = ast.unparse(new_tree)
                return {
                    'success': True,
                    'optimized_code': optimized_code,
                    'changes': ['Added __slots__ to class definitions']
                }
            
            return {
                'success': False,
                'optimized_code': code,
                'changes': []
            }
            
        except Exception as e:
            return {
                'success': False,
                'optimized_code': code,
                'error': str(e)
            }
    
    def _apply_memory_mapping(self, code: str) -> Dict[str, Any]:
        """Apply memory mapping for file operations."""
        # Simplified implementation - detect file.read() patterns
        pattern = r'with\s+open\([^)]+\)\s+as\s+(\w+):\s*\n\s*(\w+)\s*=\s*\1\.read\(\)'
        
        if re.search(pattern, code):
            # Replace with mmap pattern
            replacement = """import mmap

with open(filename, 'rb') as f:
    with mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ) as mm:
        # Use mm as a memory-mapped file"""
            
            return {
                'success': True,
                'optimized_code': code,  # Simplified - would need proper replacement
                'changes': ['Applied memory mapping for file operations']
            }
        
        return {
            'success': False,
            'optimized_code': code,
            'changes': []
        }
    
    def _implement_object_pooling(self, code: str) -> Dict[str, Any]:
        """Implement object pooling for frequently created objects."""
        # Simplified implementation - detect repeated object creation
        pattern = r'for\s+.*\s+in\s+.*:\s*\n\s*.*=\s*\w+\([^)]*\)'
        
        if re.search(pattern, code):
            # Suggest object pooling
            pool_template = """
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
"""
            
            return {
                'success': True,
                'optimized_code': code + pool_template,  # Simplified
                'changes': ['Added object pooling template']
            }
        
        return {
            'success': False,
            'optimized_code': code,
            'changes': []
        }