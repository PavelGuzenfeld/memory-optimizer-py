# Memory Optimizer

A CLI tool for automatically optimizing Python code for memory efficiency.

## Features

- 🚀 Automatic memory optimization of Python code
- 🔄 In-place file updates with backup creation
- 🧪 Automatic test generation to verify optimizations
- 📁 Directory and recursive optimization
- 📊 Detailed optimization reports
- ✅ Comprehensive test suite

## Installation

```bash
pip3 install memory-optimizer
```

## Usage

### Optimize a single file:
```bash
memopt myfile.py
```
### Optimize a directory:
```bash
memopt my_project/ --recursive
```
### Dry run (see what would change):
```bash
memopt myfile.py --dry-run
```
### Generate optimization report:
```bash
memopt my_project/ --report optimization_report.md
```
### Run tests after optimization:
```bash
memopt myfile.py --run-tests
```

### Command Line Options

- `--dry-run`: Show what would be changed without modifying files
- `--no-backup`: Don't create backup files
- `--no-tests`: Don't create test files
- `--recursive, -r`: Recursively process directories
- `--pattern PATTERN`: File pattern to match (default: *.py)
- `--verbose, -v`: Enable verbose output
- `--report FILE`: Generate optimization report
- `--run-tests`: Run tests after optimization

## Examples
### Before:
```python
def read_large_file(filename):
    with open(filename, 'r') as f:
        data = f.read()
    return [line.upper() for line in data.splitlines()]
```
### After:
```python
from typing import Generator

def read_large_file(filename: str) -> Generator[str, None, None]:
    """Process file line by line for memory efficiency."""
    with open(filename, 'r') as f:
        for line in f:
            yield line.rstrip('\n').upper()
```
