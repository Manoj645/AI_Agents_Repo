#!/usr/bin/env python3
"""
This is a test file with intentional code quality issues
to verify the AI agent's ability to detect violations.
"""

import os,sys  # Bad: multiple imports on same line
from datetime import datetime
import json
import requests

# Bad: Global variables without clear purpose
GLOBAL_VAR = "some value"
ANOTHER_GLOBAL = 123

# Bad: Function with too many parameters
def bad_function_with_many_params(param1, param2, param3, param4, param5, param6, param7, param8, param9, param10):
    """Function with too many parameters - violates single responsibility"""
    result = param1 + param2 + param3 + param4 + param5 + param6 + param7 + param8 + param9 + param10
    return result

# Bad: Function without docstring
def function_without_docstring():
    x = 10
    y = 20
    return x + y

# Bad: Inconsistent naming convention
def BadFunctionName():
    """Function with incorrect naming convention"""
    pass

# Bad: Magic numbers
def calculate_something():
    result = 42 * 7 + 13  # Magic numbers without explanation
    return result

# Bad: Long function
def very_long_function():
    """This function is too long and should be broken down"""
    x = 1
    y = 2
    z = 3
    a = 4
    b = 5
    c = 6
    d = 7
    e = 8
    f = 9
    g = 10
    h = 11
    i = 12
    j = 13
    k = 14
    l = 15
    m = 16
    n = 17
    o = 18
    p = 19
    q = 20
    r = 21
    s = 22
    t = 23
    u = 24
    v = 25
    w = 26
    x = 27
    y = 28
    z = 29
    a = 30
    b = 31
    c = 32
    d = 33
    e = 34
    f = 35
    g = 36
    h = 37
    i = 38
    j = 39
    k = 40
    l = 41
    m = 42
    n = 43
    o = 44
    p = 45
    q = 46
    r = 47
    s = 48
    t = 49
    u = 50
    v = 51
    w = 52
    x = 53
    y = 54
    z = 55
    a = 56
    b = 57
    c = 58
    d = 59
    e = 60
    f = 61
    g = 62
    h = 63
    i = 64
    j = 65
    k = 66
    l = 67
    m = 68
    n = 69
    o = 70
    p = 71
    q = 72
    r = 73
    s = 74
    t = 75
    u = 76
    v = 77
    w = 78
    x = 79
    y = 80
    z = 81
    a = 82
    b = 83
    c = 84
    d = 85
    e = 86
    f = 87
    g = 88
    h = 89
    i = 90
    j = 91
    k = 92
    l = 93
    m = 94
    n = 95
    o = 96
    p = 97
    q = 98
    r = 99
    s = 100
    return x + y + z + a + b + c + d + e + f + g + h + i + j + k + l + m + n + o + p + q + r + s + t + u + v + w

# Bad: Unused imports and variables
def unused_variables():
    """Function with unused variables"""
    unused_var = "this is never used"
    another_unused = 42
    return "only this is used"

# Bad: Hardcoded credentials
def connect_to_database():
    """Function with hardcoded credentials"""
    username = "admin"
    password = "password123"  # Bad: hardcoded password
    host = "localhost"
    return f"mysql://{username}:{password}@{host}"

# Bad: Exception handling too broad
def bad_exception_handling():
    """Function with overly broad exception handling"""
    try:
        result = 10 / 0
    except:  # Bad: bare except clause
        print("Something went wrong")

# Bad: Inconsistent indentation
def inconsistent_indentation():
    """Function with inconsistent indentation"""
    x = 1
    y = 2  # This should be properly indented
    z = 3
    return x + y + z

# Bad: No type hints
def function_without_type_hints(param1, param2):
    """Function without type hints"""
    result = param1 + param2
    return result

# Bad: String concatenation instead of f-strings
def old_string_formatting():
    """Function using old string formatting"""
    name = "John"
    age = 30
    message = "My name is " + name + " and I am " + str(age) + " years old"  # Bad: string concatenation
    return message

# Bad: Unnecessary complexity
def overly_complex_function():
    """Function with unnecessary complexity"""
    data = []
    for i in range(10):
        if i % 2 == 0:
            if i > 5:
                if i < 8:
                    data.append(i)
                else:
                    data.append(i * 2)
            else:
                data.append(i + 1)
        else:
            if i < 5:
                data.append(i - 1)
            else:
                data.append(i + 2)
    return data

# Bad: No error handling
def function_without_error_handling():
    """Function without proper error handling"""
    file = open("nonexistent_file.txt", "r")  # Bad: no error handling
    content = file.read()
    file.close()
    return content

# Bad: Inconsistent return types
def inconsistent_return_types(condition):
    """Function with inconsistent return types"""
    if condition:
        return "string"
    else:
        return 42  # Bad: mixing string and int return types

# Bad: Dead code
def function_with_dead_code():
    """Function with unreachable code"""
    return "this is returned"
    print("this will never execute")  # Bad: dead code
    return "this will never execute either"

# Bad: No logging
def function_without_logging():
    """Function without proper logging"""
    result = some_calculation()
    print("Result:", result)  # Bad: using print instead of logging
    return result

def some_calculation():
    """Helper function"""
    return 42

# Bad: Class with too many responsibilities
class BadClass:
    """Class with too many responsibilities"""
    
    def __init__(self):
        self.data = []
        self.config = {}
        self.connection = None
        self.cache = {}
        self.logger = None
    
    def process_data(self):
        """Process data"""
        pass
    
    def save_to_database(self):
        """Save to database"""
        pass
    
    def send_email(self):
        """Send email"""
        pass
    
    def generate_report(self):
        """Generate report"""
        pass
    
    def backup_files(self):
        """Backup files"""
        pass
    
    def validate_input(self):
        """Validate input"""
        pass
    
    def format_output(self):
        """Format output"""
        pass

# Bad: SQL Injection vulnerability
def vulnerable_sql_query(user_input):
    """Function vulnerable to SQL injection"""
    query = "SELECT * FROM users WHERE name = '" + user_input + "'"  # Bad: SQL injection
    return query

# Bad: Hardcoded API key
def api_call_with_hardcoded_key():
    """Function with hardcoded API key"""
    api_key = "sk-1234567890abcdef"  # Bad: hardcoded API key
    headers = {"Authorization": f"Bearer {api_key}"}
    return headers

# Bad: Insecure password hashing
def insecure_password_hash(password):
    """Function with insecure password hashing"""
    import hashlib
    return hashlib.md5(password.encode()).hexdigest()  # Bad: MD5 is insecure

# Bad: No input validation
def process_user_input(user_input):
    """Function without input validation"""
    return eval(user_input)  # Bad: eval() is dangerous

# Bad: Resource leak
def file_operation_without_context_manager():
    """Function that doesn't use context manager for file operations"""
    file = open("test.txt", "w")
    file.write("test")
    # Bad: file is never closed, causing resource leak
    return "file written"

# Bad: Inefficient algorithm
def inefficient_sort(data):
    """Function with inefficient sorting algorithm"""
    # Bad: O(n²) bubble sort instead of built-in O(n log n) sort
    for i in range(len(data)):
        for j in range(len(data) - 1):
            if data[j] > data[j + 1]:
                data[j], data[j + 1] = data[j + 1], data[j]
    return data

# Bad: Global mutable state
global_counter = 0
global_data = []

def modify_global_state():
    """Function that modifies global state"""
    global global_counter, global_data
    global_counter += 1
    global_data.append(global_counter)
    return global_counter

# Bad: Deep nesting
def deeply_nested_function():
    """Function with excessive nesting"""
    for i in range(10):
        if i > 0:
            for j in range(i):
                if j % 2 == 0:
                    for k in range(j):
                        if k < 5:
                            for l in range(k):
                                if l > 0:
                                    print(f"Deeply nested: {i}-{j}-{k}-{l}")

# Bad: Inconsistent naming conventions
def InconsistentNaming():
    """Function with inconsistent naming"""
    camelCase = "bad"
    snake_case = "good"
    UPPER_CASE = "also bad"
    return camelCase + snake_case + UPPER_CASE

# Bad: Long line exceeding 88 characters
def function_with_very_long_line_that_exceeds_the_recommended_line_length_and_should_be_broken_down_into_multiple_lines():
    """Function with line that's too long"""
    return "This line is way too long and should be broken down into multiple lines to improve readability and follow PEP 8 guidelines"

# Bad: Unused parameters
def function_with_unused_params(param1, param2, param3):
    """Function with unused parameters"""
    result = param1 + param2  # param3 is never used
    return result

# Bad: Magic strings
def function_with_magic_strings():
    """Function with magic strings"""
    if status == "ACTIVE":
        return "User is active"
    elif status == "INACTIVE":
        return "User is inactive"
    elif status == "PENDING":
        return "User is pending"
    elif status == "SUSPENDED":
        return "User is suspended"
    else:
        return "Unknown status"

# Bad: Side effects in function
def function_with_side_effects():
    """Function with side effects"""
    global global_counter
    global_counter += 1
    print(f"Counter incremented to: {global_counter}")
    return global_counter

# Bad: Duplicate code
def duplicate_function_1():
    """First duplicate function"""
    data = []
    for i in range(10):
        if i % 2 == 0:
            data.append(i * 2)
        else:
            data.append(i + 1)
    return data

def duplicate_function_2():
    """Second duplicate function (same logic)"""
    data = []
    for i in range(10):
        if i % 2 == 0:
            data.append(i * 2)
        else:
            data.append(i + 1)
    return data

# Bad: Hardcoded file paths
def read_config_file():
    """Function with hardcoded file path"""
    config_path = "/home/user/config/settings.json"
    with open(config_path, 'r') as f:
        return f.read()

# Bad: No input validation
def divide_numbers(a, b):
    """Function without input validation"""
    return a / b  # No check for b == 0

# Bad: Inefficient string operations
def inefficient_string_operations():
    """Function with inefficient string operations"""
    result = ""
    for i in range(1000):
        result += str(i)  # Bad: string concatenation in loop
    return result

# Bad: Unnecessary complexity
def unnecessarily_complex_boolean_logic():
    """Function with unnecessarily complex boolean logic"""
    condition1 = True
    condition2 = False
    condition3 = True
    condition4 = False
    
    if (condition1 and condition2) or (condition3 and condition4) or (condition1 and condition3) or (condition2 and condition4):
        return "Complex condition met"
    else:
        return "Complex condition not met"

# Bad: No main guard
if __name__ == "__main__":
    print("Running bad code test")
    bad_function_with_many_params(1,2,3,4,5,6,7,8,9,10)
    function_without_docstring()
    BadFunctionName()
    calculate_something()
    very_long_function()
    unused_variables()
    connect_to_database()
    bad_exception_handling()
    inconsistent_indentation()
    function_without_type_hints("hello", "world")
    old_string_formatting()
    overly_complex_function()
    function_without_error_handling()
    inconsistent_return_types(True)
    function_with_dead_code()
    function_without_logging()
    
    # Test new security and performance issues
    vulnerable_sql_query("admin'; DROP TABLE users; --")
    api_call_with_hardcoded_key()
    insecure_password_hash("password123")
    process_user_input("__import__('os').system('ls')")
    file_operation_without_context_manager()
    inefficient_sort([5, 2, 8, 1, 9, 3, 7, 4, 6])
    
    # Test new violations
    modify_global_state()
    deeply_nested_function()
    InconsistentNaming()
    function_with_very_long_line_that_exceeds_the_recommended_line_length_and_should_be_broken_down_into_multiple_lines()
    function_with_unused_params(1, 2, 3)
    function_with_magic_strings()
    function_with_side_effects()
    duplicate_function_1()
    duplicate_function_2()
    read_config_file()
    divide_numbers(10, 0)  # This will cause division by zero
    inefficient_string_operations()
    unnecessarily_complex_boolean_logic()
