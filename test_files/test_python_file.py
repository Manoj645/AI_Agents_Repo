"""
Test Python file for AI code review validation.
This file intentionally violates several coding standards to test the AI agent.
"""

import sys, os, json
from datetime import datetime
import requests
import sqlalchemy
from models import User
from utils import helpers

# Magic numbers without constants (violates Rule 7)
def process_data(data):
    if len(data) > 100:
        return data[:100]
    return data

# Function that's too long (violates Rule 1 - should be under 15 lines)
def calculate_user_statistics(user_data, include_inactive=False, sort_by_name=False, limit_results=None, filter_by_date=None):
    """Calculate various statistics for user data"""
    if not user_data:
        return None
    
    total_users = len(user_data)
    active_users = 0
    inactive_users = 0
    total_age = 0
    age_count = 0
    
    for user in user_data:
        if user.get('status') == 'active':
            active_users += 1
        else:
            inactive_users += 1
        
        if 'age' in user:
            total_age += user['age']
            age_count += 1
    
    avg_age = total_age / age_count if age_count > 0 else 0
    
    if include_inactive:
        result = {
            'total': total_users,
            'active': active_users,
            'inactive': inactive_users,
            'avg_age': avg_age
        }
    else:
        result = {
            'total': active_users,
            'avg_age': avg_age
        }
    
    if sort_by_name:
        result['sorted_users'] = sorted(user_data, key=lambda x: x.get('name', ''))
    
    if limit_results:
        result['limited'] = result.get('sorted_users', user_data)[:limit_results]
    
    return result

# Poor variable naming (violates Rule 2)
def calc(x, y, z):
    """Calculate something"""
    temp = x + y
    cnt = 0
    for i in range(z):
        if temp > 10:
            cnt += 1
    return cnt

# Missing error handling (violates Rule 4)
def fetch_user_data(user_id):
    """Fetch user data from API"""
    response = requests.get(f"https://api.example.com/users/{user_id}")
    return response.json()

# No type hints (violates Rule 14)
def process_items(items, limit):
    """Process a list of items"""
    result = {}
    for item in items:
        if item in result:
            result[item] += 1
        else:
            result[item] = 1
    
    if limit:
        # Complex list comprehension (violates Rule 8)
        filtered = {k: v for k, v in result.items() if v > limit and len(k) > 3 and k.isalpha() and v % 2 == 0}
        return filtered
    
    return result

# Inconsistent spacing (violates Rule 10)
def bad_formatting(a,b,c):
    result=a+b*c
    items=[1,2,3]
    return result,items

# Function without docstring (violates Rule 5)
def undocumented_function():
    x = 42
    y = x * 2
    return y

# Poor error handling with bare except (violates Rule 4)
def risky_operation(data):
    try:
        result = json.loads(data)
        return result
    except:
        return None

# Security issue: SQL injection vulnerability (violates security best practices)
def get_user_by_id(user_id):
    """Get user by ID - vulnerable to SQL injection"""
    conn = sqlalchemy.create_engine('postgresql://localhost/testdb')
    cursor = conn.execute(f"SELECT * FROM users WHERE id = '{user_id}'")
    return cursor.fetchone()

# Performance issue: Inefficient algorithm (violates Rule 12)
def find_duplicates(items):
    """Find duplicate items using O(n²) algorithm"""
    duplicates = []
    for i in range(len(items)):
        for j in range(i + 1, len(items)):
            if items[i] == items[j] and items[i] not in duplicates:
                duplicates.append(items[i])
    return duplicates

# Deep nesting (violates Rule 11 - should use early returns)
def complex_validation(data):
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

# Main execution
if __name__ == "__main__":
    # Test data
    test_users = [
        {'name': 'Alice', 'age': 25, 'status': 'active'},
        {'name': 'Bob', 'age': 30, 'status': 'inactive'},
        {'name': 'Charlie', 'age': 35, 'status': 'active'}
    ]
    
    # Call functions with violations
    stats = calculate_user_statistics(test_users, True, True, 2)
    print(f"User statistics: {stats}")
    
    result = calc(5, 3, 10)
    print(f"Calculation result: {result}")
    
    items = ['apple', 'banana', 'apple', 'cherry', 'banana']
    processed = process_items(items, 1)
    print(f"Processed items: {processed}")
