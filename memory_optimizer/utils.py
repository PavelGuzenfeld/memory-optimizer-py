"""
Utility functions for the Memory Optimizer tool.
"""

import logging
import subprocess
import sys
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime

def setup_logging(verbose: bool = False) -> None:
    """Setup logging configuration."""
    level = logging.DEBUG if verbose else logging.INFO
    
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

def format_report(results: List[Dict[str, Any]]) -> str:
    """Format optimization results as a markdown report."""
    report = ["# Memory Optimization Report\n"]
    report.append(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    # Summary
    total_files = len(results)
    optimized_files = sum(1 for r in results if r.get('changes_made', False))
    failed_files = sum(1 for r in results if 'error' in r)
    total_memory_saved = sum(r.get('memory_saved', 0) for r in results)
    
    report.append("## Summary\n")
    report.append(f"- Total files processed: {total_files}")
    report.append(f"- Files optimized: {optimized_files}")
    report.append(f"- Files unchanged: {total_files - optimized_files - failed_files}")
    report.append(f"- Failed: {failed_files}")
    report.append(f"- Average memory savings: {total_memory_saved / total_files:.1f}%\n")
    
    # Detailed results
    report.append("## Detailed Results\n")
    
    for result in results:
        file_path = result['file']
        report.append(f"### {file_path}\n")
        
        if 'error' in result:
            report.append(f"**Error**: {result['error']}\n")
            continue
        
        if result.get('changes_made', False):
            report.append(f"**Status**: Optimized")
            report.append(f"**Memory saved**: {result['memory_saved']}%")
            
            if result.get('test_file'):
                report.append(f"**Test file**: {result['test_file']}")
            
            if result.get('backup_file'):
                report.append(f"**Backup file**: {result['backup_file']}")
            
            report.append("\n**Changes made**:")
            report.append("```diff")
            report.append("- Original code")
            report.append("+ Optimized code")
            report.append("```")
        else:
            report.append("**Status**: No optimization needed")
        
        report.append("")
    
    return '\n'.join(report)

def run_tests(results: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Run tests for optimized code."""
    test_results = {
        'total': 0,
        'passed': 0,
        'failed': 0,
        'errors': []
    }
    
    for result in results:
        if not result.get('test_file'):
            continue
        
        test_file = Path(result['test_file'])
        if not test_file.exists():
            continue
        
        test_results['total'] += 1
        
        try:
            # Run the test file using unittest
            process = subprocess.run(
                [sys.executable, '-m', 'unittest', str(test_file)],
                capture_output=True,
                text=True
            )
            
            if process.returncode == 0:
                test_results['passed'] += 1
            else:
                test_results['failed'] += 1
                test_results['errors'].append({
                    'file': str(test_file),
                    'error': process.stderr
                })
        
        except Exception as e:
            test_results['failed'] += 1
            test_results['errors'].append({
                'file': str(test_file),
                'error': str(e)
            })
    
    test_results['success'] = test_results['failed'] == 0
    return test_results

def create_test_file(original_file: Path, test_code: str) -> Optional[Path]:
    """Create a test file for the optimized code."""
    if not test_code:
        return None
    
    test_file_name = f"test_{original_file.stem}.py"
    test_file_path = original_file.parent / test_file_name
    
    try:
        with open(test_file_path, 'w', encoding='utf-8') as f:
            f.write(test_code)
        return test_file_path
    except Exception as e:
        logging.error(f"Failed to create test file: {e}")
        return None

def estimate_memory_savings(original_code: str, optimized_code: str) -> float:
    """Estimate memory savings based on optimization patterns."""
    savings = 0.0
    
    # Check for generator conversion
    if 'yield' in optimized_code and 'yield' not in original_code:
        savings += 30.0
    
    # Check for __slots__ addition
    if '__slots__' in optimized_code and '__slots__' not in original_code:
        savings += 25.0
    
    # Check for memory mapping
    if 'mmap' in optimized_code and 'mmap' not in original_code:
        savings += 40.0
    
    # Check for array usage
    if 'array.array' in optimized_code and 'array.array' not in original_code:
        savings += 20.0
    
    # Check for object pooling
    if 'ObjectPool' in optimized_code and 'ObjectPool' not in original_code:
        savings += 35.0
    
    return min(savings, 90.0)  # Cap at 90% maximum savings

def validate_python_code(code: str) -> bool:
    """Validate that the code is syntactically correct Python."""
    try:
        compile(code, '<string>', 'exec')
        return True
    except SyntaxError:
        return False

def get_python_version() -> str:
    """Get the current Python version."""
    return f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"

def check_dependencies() -> Dict[str, bool]:
    """Check if required dependencies are installed."""
    dependencies = {
        'memory_profiler': False,
        'numpy': False,
        'psutil': False
    }
    
    for package in dependencies:
        try:
            __import__(package)
            dependencies[package] = True
        except ImportError:
            dependencies[package] = False
    
    return dependencies

def format_file_size(size_bytes: int) -> str:
    """Format file size in human-readable format."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f} TB"

def backup_file(file_path: Path) -> Optional[Path]:
    """Create a backup of the given file."""
    try:
        backup_path = file_path.with_suffix(file_path.suffix + '.bak')
        import shutil
        shutil.copy2(file_path, backup_path)
        return backup_path
    except Exception as e:
        logging.error(f"Failed to create backup: {e}")
        return None