# Testing Your AI Code Review Agent

This guide explains how to test your AI code review system with the provided dummy Python files.

## System Overview

Your system works as follows:
1. **GitHub Webhook** → FastAPI endpoint (`/webhooks/github`)
2. **Store PR Metadata** → PostgreSQL database (`pull_requests`, `files`, `code_reviews` tables)
3. **AI Agent** → Fetches PR files from GitHub API → Analyzes against custom rules → Stores suggestions

## Test Files Created

### 1. `test_python_file.py`
**Violations included:**
- Function length > 15 lines (`calculate_user_statistics`)
- Poor variable naming (`calc`, `temp`, `cnt`)
- Import organization issues (multiple imports on one line)
- Missing error handling (`fetch_user_data`)
- No type hints (`process_items`)
- Inconsistent spacing (`bad_formatting`)
- Missing docstrings (`undocumented_function`)
- Magic numbers without constants
- Complex list comprehensions
- SQL injection vulnerability
- Inefficient algorithms
- Deep nesting

### 2. `test_security_issues.py`
**Violations included:**
- SQL injection vulnerabilities
- Command injection
- Weak cryptography (MD5)
- Performance issues (O(n²) algorithms)
- Memory issues (loading entire files)
- Deep nesting
- Missing validation
- Side effects in functions
- Magic numbers
- Poor error handling

## How to Test Your System

### Method 1: Manual AI Review Trigger

1. **Upload test files to a GitHub repository**
   ```bash
   # Create a test repository and upload the files
   git init test-repo
   git add test_python_file.py test_security_issues.py
   git commit -m "Add test files for AI review"
   git push origin main
   ```

2. **Create a Pull Request** with changes to these files

3. **Trigger AI Review** using your API:
   ```bash
   # Get PR ID from your database or GitHub
   curl -X POST "https://your-render-app.onrender.com/ai-review/{pr_id}"
   ```

4. **Check Results**:
   ```bash
   # Get PR suggestions
   curl "https://your-render-app.onrender.com/prs/{pr_id}/suggestions"
   ```

### Method 2: Test Webhook Flow

1. **Set up GitHub webhook** pointing to your endpoint:
   ```
   URL: https://your-render-app.onrender.com/webhooks/github
   Content type: application/json
   Events: Pull requests
   ```

2. **Create/modify PR** in your test repository

3. **Check database** for stored data:
   ```sql
   -- Check PR was stored
   SELECT * FROM pull_requests ORDER BY created_at DESC LIMIT 5;
   
   -- Check files were stored
   SELECT * FROM files ORDER BY created_at DESC LIMIT 5;
   
   -- Check AI suggestions were stored
   SELECT * FROM code_reviews ORDER BY created_at DESC LIMIT 10;
   ```

### Method 3: Direct API Testing

1. **Test webhook endpoint**:
   ```bash
   curl -X POST "https://your-render-app.onrender.com/webhooks/github" \
     -H "Content-Type: application/json" \
     -H "X-GitHub-Event: pull_request" \
     -H "X-Hub-Signature-256: sha256=..." \
     -d @webhook_payload.json
   ```

2. **Test database connection**:
   ```bash
   curl "https://your-render-app.onrender.com/db-test"
   ```

3. **Get all PRs**:
   ```bash
   curl "https://your-render-app.onrender.com/prs"
   ```

## Expected AI Agent Behavior

When analyzing the test files, your AI agent should:

### For `test_python_file.py`:
- **Function Length**: Detect `calculate_user_statistics` exceeds 15 lines
- **Variable Naming**: Identify poor names like `calc`, `temp`, `cnt`
- **Import Organization**: Flag multiple imports on single line
- **Error Handling**: Note missing try-catch in `fetch_user_data`
- **Type Hints**: Identify missing type annotations
- **Formatting**: Detect inconsistent spacing in `bad_formatting`
- **Documentation**: Flag missing docstring in `undocumented_function`
- **Magic Numbers**: Identify hardcoded values without constants
- **Security**: Detect SQL injection vulnerability
- **Performance**: Flag inefficient algorithms

### For `test_security_issues.py`:
- **Security**: Detect SQL injection, command injection, weak cryptography
- **Performance**: Identify O(n²) algorithms and memory issues
- **Code Quality**: Flag deep nesting, missing validation
- **Testing**: Note side effects in functions
- **Documentation**: Identify incomplete parameter descriptions

## Custom Rules Applied

Your AI agent should reference these rules from `Custom-rules/python-code-standards.md`:

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

## Verification Checklist

After running tests, verify:

- [ ] **Webhook Processing**: PR metadata stored in database
- [ ] **File Fetching**: GitHub API successfully fetches file contents
- [ ] **AI Analysis**: Custom rules are applied correctly
- [ ] **Suggestion Storage**: AI suggestions stored in `code_reviews` table
- [ ] **API Endpoints**: All endpoints return expected data
- [ ] **Error Handling**: System handles errors gracefully
- [ ] **Performance**: AI review completes in reasonable time

## Troubleshooting

### Common Issues:

1. **GitHub API Rate Limits**: Check if you're hitting rate limits
2. **Database Connection**: Verify PostgreSQL connection in Render
3. **Environment Variables**: Ensure all required env vars are set
4. **Custom Rules Path**: Verify AI agent can access custom rules file

### Debug Endpoints:

```bash
# Check system health
curl "https://your-render-app.onrender.com/health"

# Test database connection
curl "https://your-render-app.onrender.com/db-test"

# Get all PRs
curl "https://your-render-app.onrender.com/prs"
```

## Next Steps

1. **Test with real PRs** in your actual repositories
2. **Monitor performance** and optimize if needed
3. **Add more custom rules** for different languages/file types
4. **Enhance error handling** and logging
5. **Add metrics** to track AI review effectiveness

## Notes

- These test files are intentionally flawed for validation purposes
- The AI agent should identify multiple violations in each file
- Different files test different aspects of the validation system
- Monitor your Render logs for any errors during processing
