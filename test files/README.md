# Test Files for AI Code Review Agent

This folder contains Python files designed to test your AI code review system. These files intentionally violate various coding standards defined in `Custom-rules/python-code-standards.md`.

## Files Overview

### 1. `bad_code_example.py`
**Focus**: Basic code quality violations
- **Function Length**: `calculate_user_statistics()` exceeds 15 lines
- **Variable Naming**: Poor names like `calc()`, `temp`, `cnt`
- **Import Organization**: Multiple imports on single line
- **Error Handling**: Missing try-catch blocks
- **Type Hints**: Missing type annotations
- **Formatting**: Inconsistent spacing
- **Documentation**: Missing docstrings
- **Magic Numbers**: Hardcoded values without constants
- **Security**: SQL injection vulnerability
- **Performance**: Inefficient algorithms

### 2. `security_vulnerabilities.py`
**Focus**: Security and performance issues
- **SQL Injection**: Direct string concatenation in queries
- **Command Injection**: Unsafe subprocess calls
- **Weak Cryptography**: MD5 password hashing
- **Performance**: O(n²) algorithm for finding duplicates
- **Memory Issues**: Loading entire files into memory
- **Deep Nesting**: Complex validation with many levels
- **Side Effects**: Database modifications without transactions
- **Magic Numbers**: Hardcoded values without constants
- **Poor Error Handling**: Missing exception handling

### 3. `subtle_issues.py`
**Focus**: Subtle code quality issues
- **Silent Failures**: Missing validation without proper error handling
- **Inconsistent Error Handling**: Mixed exception handling patterns
- **Missing Configuration**: Incomplete API client setup
- **Hardcoded Logic**: Business rules embedded in code
- **Inefficient Operations**: Poor algorithm choices
- **Missing Validation**: Incomplete input validation
- **Cache Issues**: No cache size limits
- **Retry Logic**: Fixed delays instead of exponential backoff

## How to Use

### Method 1: GitHub Repository Testing
1. **Upload these files** to a GitHub repository
2. **Create a Pull Request** with changes to these files
3. **GitHub webhook** will trigger your AI agent
4. **Check database** for stored suggestions

### Method 2: Manual Testing
```bash
# Test webhook endpoint
curl "https://your-render-app.onrender.com/webhook-test"

# Test database connection
curl "https://your-render-app.onrender.com/db-test"

# Get all PRs
curl "https://your-render-app.onrender.com/prs"
```

## Expected AI Agent Behavior

Your AI agent should detect violations like:

### Code Quality Issues:
- Function length exceeding 15 lines
- Poor variable naming conventions
- Missing error handling
- No type hints
- Inconsistent formatting
- Missing documentation
- Magic numbers without constants

### Security Issues:
- SQL injection vulnerabilities
- Command injection
- Weak cryptography (MD5)
- Missing input validation

### Performance Issues:
- O(n²) algorithms instead of O(n)
- Loading entire files into memory
- Inefficient data structures

### Testing Issues:
- Functions with side effects
- Hard to test code
- Missing validation

## Custom Rules Applied

These files violate rules from `Custom-rules/python-code-standards.md`:

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

## Verification Steps

After running tests, verify:

1. **Webhook Processing**: PR metadata stored in database
2. **File Fetching**: GitHub API successfully fetches file contents
3. **AI Analysis**: Custom rules are applied correctly
4. **Suggestion Storage**: AI suggestions stored in `code_reviews` table
5. **API Endpoints**: All endpoints return expected data

## Database Queries for Verification

```sql
-- Check recent PRs
SELECT id, title, repository, pr_number, created_at 
FROM pull_requests 
ORDER BY created_at DESC LIMIT 5;

-- Check AI suggestions
SELECT file_path, suggestion_type, severity, title 
FROM code_reviews 
ORDER BY created_at DESC LIMIT 10;

-- Check files
SELECT filename, status, additions, deletions 
FROM files 
ORDER BY created_at DESC LIMIT 5;
```

## Notes

- These files are intentionally flawed for testing purposes
- They should not be used as examples of good coding practices
- The AI agent should identify multiple violations in each file
- Different files focus on different types of issues
- Monitor your Render logs for any errors during processing

## Troubleshooting

If AI agent doesn't detect violations:

1. **Check custom rules file**: Ensure `Custom-rules/python-code-standards.md` is accessible
2. **Verify GitHub API**: Check if files are being fetched correctly
3. **Monitor logs**: Look for AI agent processing messages
4. **Test configuration**: Use `/ai-review/{pr_id}` endpoint to manually trigger review
