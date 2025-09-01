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
      y = 2  # Bad: wrong indentation
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
