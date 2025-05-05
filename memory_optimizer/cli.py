#!/usr/bin/env python3
"""
Memory Optimizer CLI Tool
A command-line tool for optimizing Python code for memory efficiency.
"""

import argparse
import sys
import os
import shutil
import logging
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional, Any

from .agent import MemoryOptimizationAgent
from .backup import BackupManager
from .analyzer import CodeAnalyzer
from .utils import (
    setup_logging, 
    format_report, 
    run_tests, 
    create_test_file
)

class MemoryOptimizerCLI:
    """Command-line interface for the memory optimization tool."""
    
    def __init__(self):
        self.agent = MemoryOptimizationAgent()
        self.backup_manager = BackupManager()
        self.analyzer = CodeAnalyzer()
        
    def optimize_file(self, file_path: Path, dry_run: bool = False, 
                     create_tests: bool = True) -> Dict[str, Any]:
        """Optimize a single Python file."""
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        if not file_path.suffix == '.py':
            raise ValueError(f"Not a Python file: {file_path}")
        
        # Read original code
        with open(file_path, 'r', encoding='utf-8') as f:
            original_code = f.read()
        
        # Create backup
        if not dry_run:
            backup_path = self.backup_manager.create_backup(file_path)
        
        # Analyze and optimize
        analysis = self.analyzer.analyze_code(original_code)
        result = self.agent.optimize_code(original_code)
        
        # Create test file
        test_file_path = None
        if create_tests and result.test_code:
            test_file_path = create_test_file(file_path, result.test_code)
        
        # Update file if not dry-run
        if not dry_run and result.optimized_code != original_code:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(result.optimized_code)
        
        return {
            'file': str(file_path),
            'original_code': original_code,
            'optimized_code': result.optimized_code,
            'memory_saved': result.memory_saved,
            'test_file': str(test_file_path) if test_file_path else None,
            'backup_file': str(backup_path) if not dry_run else None,
            'changes_made': result.optimized_code != original_code
        }
    
    def optimize_directory(self, directory: Path, recursive: bool = True, 
                          dry_run: bool = False, pattern: str = "*.py") -> List[Dict[str, Any]]:
        """Optimize all Python files in a directory."""
        results = []
        
        if recursive:
            py_files = list(directory.rglob(pattern))
        else:
            py_files = list(directory.glob(pattern))
        
        for py_file in py_files:
            # Skip test files and backup files
            if 'test_' in py_file.name or py_file.name.endswith('.bak.py'):
                continue
                
            try:
                result = self.optimize_file(py_file, dry_run=dry_run)
                results.append(result)
            except Exception as e:
                logging.error(f"Error optimizing {py_file}: {e}")
                results.append({
                    'file': str(py_file),
                    'error': str(e),
                    'changes_made': False
                })
        
        return results

def main():
    parser = argparse.ArgumentParser(description='Memory Optimizer - Optimize Python code for memory efficiency')
    parser.add_argument('path', type=str, help='File or directory to optimize')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be changed without modifying files')
    parser.add_argument('--no-backup', action='store_true', help='Don\'t create backup files')
    parser.add_argument('--no-tests', action='store_true', help='Don\'t create test files')
    parser.add_argument('--recursive', '-r', action='store_true', help='Recursively process directories')
    parser.add_argument('--pattern', default='*.py', help='File pattern to match (default: *.py)')
    parser.add_argument('--verbose', '-v', action='store_true', help='Enable verbose output')
    parser.add_argument('--report', type=str, help='Generate optimization report to specified file')
    parser.add_argument('--run-tests', action='store_true', help='Run tests after optimization')
    
    args = parser.parse_args()
    
    # Setup logging
    setup_logging(verbose=args.verbose)
    
    # Initialize CLI
    cli = MemoryOptimizerCLI()
    
    # Check if path is file or directory
    path = Path(args.path)
    
    if path.is_file():
        results = [cli.optimize_file(path, dry_run=args.dry_run, create_tests=not args.no_tests)]
    elif path.is_dir():
        results = cli.optimize_directory(
            path, 
            recursive=args.recursive,
            dry_run=args.dry_run,
            pattern=args.pattern
        )
    else:
        print(f"Error: {path} is not a valid file or directory")
        sys.exit(1)
    
    # Display results
    total_files = len(results)
    optimized_files = sum(1 for r in results if r.get('changes_made', False))
    failed_files = sum(1 for r in results if 'error' in r)
    
    print(f"\nOptimization Summary:")
    print(f"  Total files processed: {total_files}")
    print(f"  Files optimized: {optimized_files}")
    print(f"  Files unchanged: {total_files - optimized_files - failed_files}")
    print(f"  Failed: {failed_files}")
    
    if optimized_files > 0:
        print(f"\nOptimized files:")
        for result in results:
            if result.get('changes_made', False):
                print(f"  {result['file']} - {result['memory_saved']}% memory saved")
    
    if failed_files > 0:
        print(f"\nFailed files:")
        for result in results:
            if 'error' in result:
                print(f"  {result['file']} - {result['error']}")
    
    # Generate report if requested
    if args.report:
        report_path = Path(args.report)
        report_content = format_report(results)
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report_content)
        print(f"\nReport generated: {report_path}")
    
    # Run tests if requested
    if args.run_tests and optimized_files > 0:
        print("\nRunning tests on optimized code...")
        test_results = run_tests(results)
        if test_results['passed']:
            print(f"✓ All {test_results['total']} tests passed")
        else:
            print(f"✗ {test_results['failed']} out of {test_results['total']} tests failed")
            sys.exit(1)

if __name__ == '__main__':
    main()