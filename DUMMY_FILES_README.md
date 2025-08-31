# Dummy Python Files for AI Code Review Testing

This directory contains dummy Python files designed to test the AI code review agent's validation capabilities. These files intentionally violate various coding standards defined in `Custom-rules/python-code-standards.md`.

## Files Overview

### 1. `dummy_code_for_review.py`
**Focus**: Basic code quality violations
- **Function Length**: `calculate_user_statistics()` exceeds 15 lines
- **Variable Naming**: Poor names like `calc()`, `temp`, `cnt`
- **Import Organization**: Multiple imports on single line
- **Error Handling**: Missing try-catch blocks
- **Type Hints**: Missing type annotations
- **Formatting**: Inconsistent spacing
- **Documentation**: Missing docstrings
- **Magic Numbers**: Hardcoded values without constants

### 2. `dummy_code_with_security_issues.py`
**Focus**: Security and performance issues
- **SQL Injection**: Direct string concatenation in queries
- **Command Injection**: Unsafe subprocess calls
- **Weak Cryptography**: MD5 password hashing
- **Performance**: O(n²) algorithm for finding duplicates
- **Memory Issues**: Loading entire files into memory
- **Deep Nesting**: Complex validation with many levels
- **Side Effects**: Database modifications without transactions

### 3. `dummy_code_with_subtle_issues.py`
**Focus**: Subtle code quality issues
- **Silent Failures**: Missing validation without proper error handling
- **Inconsistent Error Handling**: Mixed exception handling patterns
- **Missing Configuration**: Incomplete API client setup
- **Hardcoded Logic**: Business rules embedded in code
- **Inefficient Operations**: Poor algorithm choices
- **Missing Validation**: Incomplete input validation

## How to Use with AI Agent

### Method 1: Direct File Analysis
```python
from Api.ai_agent.code_analyzer import CodeAnalyzer
from Api.ai_agent.models import GitHubFileContent

# Initialize the analyzer
analyzer = CodeAnalyzer()

# Create file content object
file_content = GitHubFileContent(
    filename="dummy_code_for_review.py",
    content=open("dummy_code_for_review.py").read(),
    encoding="utf-8",
    size=len(open("dummy_code_for_review.py").read()),
    sha="dummy_sha",
    url="dummy_url",
    git_url="dummy_git_url",
    html_url="dummy_html_url",
    download_url="dummy_download_url"
)

# Analyze the file
suggestions = analyzer.analyze_file(
    file_content=file_content,
    repository="test-repo",
    branch="main"
)

# Print suggestions
for suggestion in suggestions:
    print(f"Type: {suggestion.suggestion_type}")
    print(f"Severity: {suggestion.severity}")
    print(f"Title: {suggestion.title}")
    print(f"Description: {suggestion.description}")
    print(f"Suggestion: {suggestion.suggestion}")
    print(f"Line: {suggestion.line_number}")
    print("---")
```

### Method 2: Using the Service Layer
```python
from Api.ai_agent.service import AICodeReviewService

# Initialize the service
service = AICodeReviewService()

# Analyze a file
with open("dummy_code_for_review.py", "r") as f:
    content = f.read()

result = service.analyze_single_file(
    filename="dummy_code_for_review.py",
    content=content,
    repository="test-repo",
    branch="main"
)

print(f"Found {len(result.suggestions)} suggestions")
```

## Expected Violations

### Code Quality Rules Violated:
1. **Function Length**: Functions exceeding 15 lines
2. **Variable Naming**: Non-descriptive names
3. **Import Organization**: Poor import structure
4. **Error Handling**: Missing or inadequate exception handling
5. **Documentation**: Missing or incomplete docstrings
6. **Magic Numbers**: Hardcoded values without constants
7. **Formatting**: Inconsistent spacing and style
8. **Type Hints**: Missing type annotations

### Security Issues:
1. **SQL Injection**: String concatenation in queries
2. **Command Injection**: Unsafe subprocess execution
3. **Weak Cryptography**: Use of broken hash functions
4. **Input Validation**: Missing or inadequate validation

### Performance Issues:
1. **Algorithm Complexity**: O(n²) instead of O(n) solutions
2. **Memory Usage**: Loading large files entirely into memory
3. **Inefficient Operations**: Poor data structure choices

### Testing Issues:
1. **Side Effects**: Functions that modify external state
2. **Hard to Test**: Functions with dependencies not easily mocked
3. **Missing Validation**: Incomplete input validation

## Custom Rules Applied

These files are designed to trigger violations based on the rules defined in `Custom-rules/python-code-standards.md`:

- **Rule 1**: Function Length & Complexity
- **Rule 2**: Variable Naming Conventions
- **Rule 3**: Import Organization
- **Rule 4**: Error Handling
- **Rule 5**: Documentation Standards
- **Rule 6**: Single Responsibility Principle
- **Rule 7**: Magic Numbers Elimination
- **Rule 8**: List/Dict Comprehensions
- **Rule 9**: Line Length
- **Rule 10**: Consistent Spacing
- **Rule 11**: Early Returns
- **Rule 12**: Efficient Data Structures
- **Rule 13**: Testable Code
- **Rule 14**: Type Hints
- **Rule 15**: Code Comments

## Testing Different Scenarios

1. **Basic Quality Issues**: Use `dummy_code_for_review.py`
2. **Security Vulnerabilities**: Use `dummy_code_with_security_issues.py`
3. **Subtle Problems**: Use `dummy_code_with_subtle_issues.py`
4. **Mixed Issues**: Analyze all three files together

## Expected AI Agent Behavior

The AI agent should:
1. **Detect Violations**: Identify specific rule violations
2. **Provide Context**: Reference the custom rules being violated
3. **Suggest Improvements**: Offer specific, actionable recommendations
4. **Categorize Issues**: Classify by type (improvement/bug/style/security/performance)
5. **Assign Severity**: Rate issues as low/medium/high/critical
6. **Reference Lines**: Point to specific line numbers where issues occur

## Notes

- These files are intentionally flawed for testing purposes
- They should not be used as examples of good coding practices
- The AI agent should identify multiple violations in each file
- Different files focus on different types of issues to test comprehensive validation
