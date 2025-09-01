"""
Subtle code quality issues for AI code review testing.
This file contains less obvious violations that require careful analysis.
"""

import logging
import time
from typing import Optional, List, Dict, Any
from dataclasses import dataclass

# Constants that should be defined but aren't
MAX_RETRIES = 3
TIMEOUT_SECONDS = 30

@dataclass
class User:
    """User data class with missing validation"""
    name: str
    email: str
    age: int
    # Missing validation for email format and age range

class DataProcessor:
    """Data processor with subtle issues"""
    
    def __init__(self):
        self.cache = {}  # No cache size limit
        self.logger = logging.getLogger(__name__)
    
    def process_data(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Process data with potential issues"""
        if not data:
            return []
        
        processed = []
        for item in data:
            # Missing validation for required fields
            if 'id' not in item:
                continue  # Silent failure
            
            # Inconsistent error handling
            try:
                processed_item = self._transform_item(item)
                processed.append(processed_item)
            except KeyError:
                # Log error but continue processing
                self.logger.warning(f"Missing key in item: {item}")
                continue
            except Exception as e:
                # Generic exception handling
                self.logger.error(f"Error processing item: {e}")
                continue
        
        return processed
    
    def _transform_item(self, item: Dict[str, Any]) -> Dict[str, Any]:
        """Transform individual item"""
        # Hardcoded business logic
        if item.get('status') == 'pending':
            item['priority'] = 'high'
        elif item.get('status') == 'completed':
            item['priority'] = 'low'
        else:
            item['priority'] = 'medium'
        
        return item

class APIClient:
    """API client with subtle issues"""
    
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.session = None  # Lazy initialization
    
    def get_data(self, endpoint: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Get data from API with potential issues"""
        if not self.session:
            self.session = self._create_session()
        
        url = f"{self.base_url}/{endpoint}"
        
        # No timeout specified
        response = self.session.get(url, params=params)
        
        # No status code validation
        return response.json()
    
    def _create_session(self):
        """Create session with missing configuration"""
        import requests
        session = requests.Session()
        # Missing headers, timeout, retry configuration
        return session

def calculate_statistics(numbers: List[float]) -> Dict[str, float]:
    """Calculate statistics with potential issues"""
    if not numbers:
        return {}
    
    # No validation for empty list after filtering
    positive_numbers = [n for n in numbers if n > 0]
    
    if not positive_numbers:
        return {}
    
    # Potential division by zero not handled
    mean = sum(positive_numbers) / len(positive_numbers)
    
    # Inefficient variance calculation
    variance = sum((x - mean) ** 2 for x in positive_numbers) / len(positive_numbers)
    
    return {
        'mean': mean,
        'variance': variance,
        'count': len(positive_numbers)
    }

def validate_email(email: str) -> bool:
    """Email validation with incomplete logic"""
    if not email:
        return False
    
    # Basic validation only
    if '@' not in email:
        return False
    
    parts = email.split('@')
    if len(parts) != 2:
        return False
    
    # Missing validation for domain format
    return True

def retry_operation(func, max_attempts: int = 3):
    """Retry decorator with potential issues"""
    def wrapper(*args, **kwargs):
        for attempt in range(max_attempts):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                if attempt == max_attempts - 1:
                    raise e
                time.sleep(1)  # Fixed delay, no exponential backoff
        return None
    return wrapper

@retry_operation
def unreliable_function():
    """Function that might fail"""
    import random
    if random.random() < 0.5:
        raise ValueError("Random failure")
    return "success"

def process_config(config: Dict[str, Any]) -> Dict[str, Any]:
    """Process configuration with missing validation"""
    # No validation for required fields
    processed_config = {}
    
    # Silent failure for missing keys
    processed_config['timeout'] = config.get('timeout', 30)
    processed_config['retries'] = config.get('retries', 3)
    processed_config['debug'] = config.get('debug', False)
    
    # No validation for value ranges
    return processed_config

def format_message(template: str, **kwargs) -> str:
    """Format message with potential issues"""
    # No validation for template format
    try:
        return template.format(**kwargs)
    except KeyError:
        # Return original template instead of proper error handling
        return template

# Main execution
if __name__ == "__main__":
    # Test the functions
    processor = DataProcessor()
    
    test_data = [
        {'id': 1, 'status': 'pending', 'name': 'Alice'},
        {'id': 2, 'status': 'completed', 'name': 'Bob'},
        {'status': 'active', 'name': 'Charlie'}  # Missing id
    ]
    
    processed = processor.process_data(test_data)
    print(f"Processed data: {processed}")
    
    # Test statistics
    numbers = [1.0, 2.0, 3.0, -1.0, 4.0]
    stats = calculate_statistics(numbers)
    print(f"Statistics: {stats}")
    
    # Test email validation
    emails = ['test@example.com', 'invalid-email', '', 'test@']
    for email in emails:
        is_valid = validate_email(email)
        print(f"Email '{email}' is valid: {is_valid}")
    
    # Test unreliable function
    try:
        result = unreliable_function()
        print(f"Function result: {result}")
    except Exception as e:
        print(f"Function failed: {e}")
