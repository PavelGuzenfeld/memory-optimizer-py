# tests/fixtures/sample_code.py

"""
Sample code snippets for testing.
"""

FILE_OPERATION_CODE = '''
def read_file(filename):
    with open(filename, 'r') as f:
        data = f.read()
    return [line.upper() for line in data.splitlines()]
'''

CLASS_WITHOUT_SLOTS = '''
class Person:
    def __init__(self, name, age, email):
        self.name = name
        self.age = age
        self.email = email
'''

LIST_COMPREHENSION_CODE = '''
def process_numbers(numbers):
    return [n * 2 for n in numbers if n > 0]
'''

NESTED_COMPREHENSION_CODE = '''
def flatten_matrix(matrix):
    return [item for row in matrix for item in row]
'''

COMPLEX_CLASS_CODE = '''
class Employee:
    def __init__(self, name, age, email, address, salary, department):
        self.name = name
        self.age = age
        self.email = email
        self.address = address
        self.salary = salary
        self.department = department
        self.projects = []
        self.skills = []
'''

LARGE_DATA_STRUCTURE_CODE = '''
def create_large_list():
    return list(range(1000000))
'''

FILE_WITH_READLINES = '''
def process_file_lines(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
    return [line.strip().upper() for line in lines]
'''

MULTIPLE_LIST_COMPREHENSIONS = '''
def process_data(data):
    filtered = [x for x in data if x > 0]
    squared = [x**2 for x in filtered]
    return [x for x in squared if x < 1000]
'''

MIXED_OPTIMIZATION_OPPORTUNITIES = '''
class DataProcessor:
    def __init__(self, name):
        self.name = name
        self.cache = {}
        
    def process_file(self, filename):
        with open(filename, 'r') as f:
            data = f.read()
        lines = data.splitlines()
        return [line.upper() for line in lines if line.strip()]
        
    def process_numbers(self, numbers):
        return [n * 2 for n in numbers if n > 0]
'''

ALREADY_OPTIMIZED_CODE = '''
from typing import Generator

class OptimizedClass:
    __slots__ = ['name', 'value']
    
    def __init__(self, name: str, value: int):
        self.name = name
        self.value = value

def optimized_file_reader(filename: str) -> Generator[str, None, None]:
    with open(filename, 'r') as f:
        for line in f:
            yield line.strip()
'''

SYNTAX_ERROR_CODE = '''
def invalid_function(
    print("This won't compile"
'''

SIMPLE_FUNCTION_CODE = '''
def add(x, y):
    return x + y

def multiply(x, y):
    return x * y
'''