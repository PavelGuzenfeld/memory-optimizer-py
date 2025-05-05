"""
Code analysis utilities for the Memory Optimizer tool.
"""

import ast
import re
from typing import Dict, List, Any

class CodeAnalyzer:
    """Analyzes Python code for memory optimization opportunities."""
    
    def analyze_code(self, code: str) -> Dict[str, Any]:
        """Analyze code for memory optimization opportunities."""
        analysis = {
            'has_file_operations': False,
            'has_list_comprehensions': False,
            'has_large_data_structures': False,
            'has_classes': False,
            'memory_issues': []
        }
        
        try:
            tree = ast.parse(code)
            
            # Check for file operations
            if self._check_file_operations(tree):
                analysis['has_file_operations'] = True
                analysis['memory_issues'].append('File loading into memory')
            
            # Check for list comprehensions
            if self._check_list_comprehensions(tree):
                analysis['has_list_comprehensions'] = True
                analysis['memory_issues'].append('Memory-intensive list comprehensions')
            
            # Check for classes without __slots__
            if self._check_classes(tree):
                analysis['has_classes'] = True
                analysis['memory_issues'].append('Classes without __slots__')
            
            # Check for large data structures
            if self._check_large_data_structures(code):
                analysis['has_large_data_structures'] = True
                analysis['memory_issues'].append('Large data structures in memory')
            
        except SyntaxError:
            analysis['error'] = 'Syntax error in code'
        
        return analysis
    
    def _check_file_operations(self, tree: ast.AST) -> bool:
        """Check for file operations that load entire files into memory."""
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                if hasattr(node.func, 'attr') and node.func.attr in ['read', 'readlines']:
                    return True
        return False
    
    def _check_list_comprehensions(self, tree: ast.AST) -> bool:
        """Check for list comprehensions that could be generators."""
        for node in ast.walk(tree):
            if isinstance(node, ast.ListComp):
                return True
        return False
    
    def _check_classes(self, tree: ast.AST) -> bool:
        """Check for classes without __slots__."""
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                has_slots = any(
                    isinstance(item, ast.Assign) and 
                    any(target.id == '__slots__' for target in item.targets if hasattr(target, 'id'))
                    for item in node.body
                )
                if not has_slots:
                    return True
        return False
    
    def _check_large_data_structures(self, code: str) -> bool:
        """Check for large data structures loaded into memory."""
        patterns = [
            r'\.read\(\)\.split',
            r'list\(.*range\(\d{5,}\)\)',
            r'\[\s*.*\s*for\s+.*\s+in\s+.*\s+if\s+.*\s*\]'
        ]
        
        for pattern in patterns:
            if re.search(pattern, code):
                return True
        return False