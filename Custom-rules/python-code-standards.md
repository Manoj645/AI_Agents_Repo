# Python Code Standards for AI Code Review

## 🎯 **Code Quality Rules**

### **1. Function Length & Complexity**
- **Rule**: Functions should not exceed 15 lines of code
- **Reason**: Improves readability, testability, and maintainability
- **Example**: Break large functions into smaller, focused functions

### **2. Variable Naming Conventions**
- **Rule**: Use descriptive, snake_case names for variables and functions
- **Reason**: Enhances code readability and understanding
- **Examples**:
  - ✅ `user_count`, `calculate_total_price()`
  - ❌ `cnt`, `calc()`, `temp`

### **3. Import Organization**
- **Rule**: Group imports: standard library, third-party, local modules
- **Reason**: Clear dependency structure and easier maintenance
- **Example**:
  ```python
  import os
  import sys
  from datetime import datetime
  
  import requests
  import sqlalchemy
  
  from models import User
  from utils import helpers
  ```

### **4. Error Handling**
- **Rule**: Always handle exceptions with specific error types
- **Reason**: Prevents crashes and provides meaningful error messages
- **Example**:
  ```python
  try:
      result = process_data(data)
  except ValueError as e:
      logger.error(f"Invalid data format: {e}")
      return None
  ```

### **5. Documentation Standards**
- **Rule**: All functions must have docstrings explaining purpose and parameters
- **Reason**: Enables better code understanding and maintenance
- **Example**:
  ```python
  def calculate_discount(price: float, discount_rate: float) -> float:
      """Calculate final price after applying discount.
      
      Args:
          price: Original price
          discount_rate: Discount percentage (0.0 to 1.0)
          
      Returns:
          Final price after discount
      """
  ```

## 🔧 **Code Structure Rules**

### **6. Single Responsibility Principle**
- **Rule**: Each function should do one thing well
- **Reason**: Easier to test, debug, and maintain
- **Example**: Separate data validation, processing, and output functions

### **7. Magic Numbers Elimination**
- **Rule**: Replace magic numbers with named constants
- **Reason**: Improves code readability and maintainability
- **Example**:
  ```python
  MAX_RETRY_ATTEMPTS = 3
  DEFAULT_TIMEOUT = 30
  
  for attempt in range(MAX_RETRY_ATTEMPTS):
      if attempt == MAX_RETRY_ATTEMPTS - 1:
          raise TimeoutError()
  ```

### **8. List/Dict Comprehensions**
- **Rule**: Use comprehensions for simple transformations (max 2 lines)
- **Reason**: More readable than traditional loops for simple operations
- **Example**:
  ```python
  # ✅ Good - Simple transformation
  squares = [x**2 for x in numbers if x > 0]
  
  # ❌ Bad - Too complex
  squares = [x**2 for x in numbers if x > 0 and x % 2 == 0 and x < 100]
  ```

## 📝 **Formatting & Style Rules**

### **9. Line Length**
- **Rule**: Maximum 88 characters per line (Black formatter standard)
- **Reason**: Ensures code fits in most editors and improves readability
- **Example**: Break long lines at logical points

### **10. Consistent Spacing**
- **Rule**: Use consistent spacing around operators and after commas
- **Reason**: Improves code readability and consistency
- **Example**:
  ```python
  # ✅ Good
  result = a + b * c
  items = [1, 2, 3]
  
  # ❌ Bad
  result=a+b*c
  items=[1,2,3]
  ```

## 🚀 **Performance Rules**

### **11. Early Returns**
- **Rule**: Use early returns to reduce nesting and improve readability
- **Reason**: Flatter code structure is easier to follow
- **Example**:
  ```python
  def process_user(user):
      if not user:
          return None
      if not user.is_active:
          return None
      # Main logic here
      return process_active_user(user)
  ```

### **12. Efficient Data Structures**
- **Rule**: Choose appropriate data structures for the use case
- **Reason**: Improves performance and memory usage
- **Examples**:
  - Sets for unique items and membership testing
  - Lists for ordered, indexed access
  - Dictionaries for key-value lookups

## 🧪 **Testing & Quality Rules**

### **13. Testable Code**
- **Rule**: Write functions that are easy to unit test
- **Reason**: Ensures code quality and enables automated testing
- **Example**: Avoid side effects, use dependency injection

### **14. Type Hints**
- **Rule**: Use type hints for function parameters and return values
- **Reason**: Improves code documentation and enables better IDE support
- **Example**:
  ```python
  def process_items(items: List[str], limit: Optional[int] = None) -> Dict[str, int]:
      """Process list of items and return frequency count."""
  ```

### **15. Code Comments**
- **Rule**: Write comments explaining "why", not "what"
- **Reason**: Code should be self-documenting; comments explain intent
- **Example**:
  ```python
  # Use 0.95 confidence interval for production systems
  confidence_level = 0.95
  
  # Skip validation for admin users to improve performance
  if user.is_admin:
      return True
  ```

## 📊 **Review Checklist**

When reviewing Python code, check for:
- [ ] Functions under 15 lines
- [ ] Clear, descriptive naming
- [ ] Proper error handling
- [ ] Comprehensive docstrings
- [ ] No magic numbers
- [ ] Consistent formatting
- [ ] Type hints usage
- [ ] Testable structure
- [ ] Performance considerations
- [ ] Code readability

## 🎯 **AI Review Focus Areas**

For AI-powered code review, prioritize:
1. **Function complexity** (length and nesting)
2. **Naming conventions** and clarity
3. **Error handling** completeness
4. **Documentation** quality
5. **Code structure** and organization

These rules ensure maintainable, readable, and high-quality Python code that follows industry best practices.
