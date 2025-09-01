"""
Security vulnerabilities and performance issues for AI code review testing.
This file contains intentional security flaws and performance problems.
"""

import subprocess
import os
import sqlite3
import hashlib
import base64
from typing import List, Dict, Any

# Security issue: SQL injection vulnerability
def get_user_by_id(user_id: str) -> Dict[str, Any]:
    """Get user by ID - vulnerable to SQL injection"""
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    # VULNERABLE: Direct string concatenation
    query = f"SELECT * FROM users WHERE id = '{user_id}'"
    cursor.execute(query)
    
    result = cursor.fetchone()
    conn.close()
    return dict(result) if result else {}

# Security issue: Command injection
def execute_command(command: str) -> str:
    """Execute system command - vulnerable to command injection"""
    # VULNERABLE: Direct command execution
    result = subprocess.check_output(command, shell=True)
    return result.decode('utf-8')

# Security issue: Weak password hashing
def hash_password(password: str) -> str:
    """Hash password using weak method"""
    # VULNERABLE: Using MD5 which is cryptographically broken
    return hashlib.md5(password.encode()).hexdigest()

# Performance issue: Inefficient algorithm
def find_duplicates(items: List[str]) -> List[str]:
    """Find duplicate items using O(n²) algorithm"""
    duplicates = []
    for i in range(len(items)):
        for j in range(i + 1, len(items)):
            if items[i] == items[j] and items[i] not in duplicates:
                duplicates.append(items[i])
    return duplicates

# Performance issue: Loading entire file into memory
def process_large_file(filename: str) -> List[str]:
    """Process large file by loading everything into memory"""
    # PERFORMANCE ISSUE: Loads entire file into memory
    with open(filename, 'r') as f:
        lines = f.readlines()  # Could cause memory issues with large files
    
    processed_lines = []
    for line in lines:
        if line.strip():
            processed_lines.append(line.strip().upper())
    
    return processed_lines

# Code quality issue: Deep nesting
def complex_validation(data: Dict[str, Any]) -> bool:
    """Complex validation with deep nesting"""
    if data:
        if 'user' in data:
            user = data['user']
            if user:
                if 'profile' in user:
                    profile = user['profile']
                    if profile:
                        if 'email' in profile:
                            email = profile['email']
                            if email:
                                if '@' in email:
                                    if '.' in email.split('@')[1]:
                                        return True
    return False

# Documentation issue: Missing parameter descriptions
def calculate_discount(price: float, discount_rate: float) -> float:
    """Calculate final price after applying discount.
    
    Args:
        price: Original price
        discount_rate: Discount percentage
        
    Returns:
        Final price after discount
    """
    # Missing validation for discount_rate range
    return price * (1 - discount_rate)

# Testing issue: Hard to test function with side effects
def update_user_status(user_id: str, status: str) -> bool:
    """Update user status with side effects"""
    # SIDE EFFECT: Direct database modification without transaction
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    cursor.execute("UPDATE users SET status = ? WHERE id = ?", (status, user_id))
    conn.commit()
    conn.close()
    
    return True

# Magic numbers without constants
def validate_age(age: int) -> bool:
    """Validate user age"""
    if age < 13:  # Magic number
        return False
    if age > 120:  # Magic number
        return False
    return True

# Poor error handling
def divide_numbers(a: float, b: float) -> float:
    """Divide two numbers without proper error handling"""
    return a / b  # No handling for division by zero

# Main execution
if __name__ == "__main__":
    # Test the vulnerable functions
    try:
        # Test SQL injection vulnerability
        user = get_user_by_id("1' OR '1'='1")
        print(f"User: {user}")
        
        # Test command injection
        result = execute_command("echo 'test'")
        print(f"Command result: {result}")
        
        # Test weak password hashing
        hashed = hash_password("password123")
        print(f"Hashed password: {hashed}")
        
        # Test inefficient algorithm
        items = ['a', 'b', 'a', 'c', 'b', 'd']
        duplicates = find_duplicates(items)
        print(f"Duplicates: {duplicates}")
        
    except Exception as e:
        print(f"Error: {e}")
