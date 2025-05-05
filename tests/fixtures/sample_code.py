# tests/fixtures/sample_code.py

```python
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
