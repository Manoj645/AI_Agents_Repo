# AI Code Review Agent

This module provides AI-powered code review functionality using LangChain and OpenAI to automatically analyze pull requests and generate code quality suggestions.

## 🏗️ Architecture

```
GitHub Webhook → Store PR Data → Trigger AI Agent → Analyze Code → Store Suggestions
     ↓              ↓              ↓           ↓           ↓
  webhooks.py   database.py   ai_agent/    LangChain   code_reviews
                                    ↓
                              GitHub API (fetch diffs + context)
```

## 📁 Module Structure

- **`config.py`** - Configuration management and environment variables
- **`models.py`** - Data models for AI suggestions and GitHub responses
- **`github_client.py`** - GitHub API client for fetching PR diffs and file contents
- **`code_analyzer.py`** - Core LangChain AI agent for code analysis
- **`review_generator.py`** - Main orchestrator for the review process
- **`service.py`** - Service layer for database integration
- **`__main__.py`** - Command-line interface for testing

## 🔧 Setup

### 1. Environment Variables

Add these to your `config.env` file:

```bash
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4o-mini  # or gpt-3.5-turbo

# GitHub Configuration
GITHUB_TOKEN=your_github_token_here

# Optional AI Configuration
MAX_TOKENS=4000
TEMPERATURE=0.1
CONTEXT_LINES=5
MAX_FILE_SIZE=1000000
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Database Migration

Run the migration to create the `code_reviews` table:

```bash
python migrate_code_reviews_table.py
```

## 🚀 Usage

### Automatic Review (Webhook Integration)

The AI agent automatically runs when a GitHub webhook is received:

1. Webhook stores PR metadata
2. AI agent is triggered automatically
3. Code analysis runs against your custom rules
4. Suggestions are stored in the database

### Manual Review

Trigger a review manually via API:

```bash
POST /ai-review/{pr_id}
```

### Command Line Testing

Test the AI agent directly:

```bash
cd Api
python -m ai_agent Manoj645 AI_Agents_Repo 123
```

## 📊 API Endpoints

- **`GET /prs/{pr_id}/suggestions`** - Get AI review suggestions for a PR
- **`POST /ai-review/{pr_id}`** - Manually trigger AI review
- **`GET /db-test`** - Test database connection and table status

## 🎯 Custom Rules

The AI agent uses rules from `Custom-rules/python-code-standards.md`. You can:

1. Modify the existing rules file
2. Update the `CUSTOM_RULES_PATH` in config
3. The agent will automatically reload rules

## 🔍 How It Works

1. **GitHub Integration**: Fetches PR diffs and file contents via GitHub API
2. **Context Analysis**: Analyzes changed lines with surrounding context
3. **AI Review**: Uses LangChain + OpenAI to analyze code against custom rules
4. **Smart Filtering**: Only stores meaningful suggestions (filters out "looks good")
5. **Database Storage**: Stores suggestions with GitHub links for easy navigation

## 📝 Output Format

Each suggestion includes:

- **File path** and **line number**
- **Suggestion type** (improvement, bug, style, security, etc.)
- **Severity level** (low, medium, high, critical)
- **Title** and **description**
- **Specific suggestion** for improvement
- **GitHub URL** linking directly to the relevant line
- **Rule applied** from your custom standards

## 🚨 Error Handling

- **Configuration validation** on startup
- **Graceful fallbacks** for missing files or API errors
- **Non-blocking webhook processing** (AI review runs in background)
- **Detailed error logging** for debugging

## 🔧 Configuration Options

- **`CONTEXT_LINES`**: Lines before/after diff for context (default: 5)
- **`MAX_FILE_SIZE`**: Maximum file size to analyze (default: 1MB)
- **`TEMPERATURE`**: AI creativity level (default: 0.1 for consistent results)
- **`MAX_TOKENS`**: Maximum tokens for AI response (default: 4000)

## 🧪 Testing

Test the AI agent with:

```bash
# Test configuration
python -c "from ai_agent.config import AIConfig; print(AIConfig.validate())"

# Test GitHub client
python -c "from ai_agent.github_client import GitHubClient; print('GitHub client ready')"

# Test code analyzer
python -c "from ai_agent.code_analyzer import CodeAnalyzer; print('Code analyzer ready')"
```

## 📚 Dependencies

- **LangChain**: AI framework for code analysis
- **OpenAI**: LLM provider for code review
- **GitHub API**: Fetch PR diffs and file contents
- **SQLAlchemy**: Database operations
- **FastAPI**: Web framework integration

## 🎉 What You Get

✅ **Automatic code reviews** on every PR  
✅ **Custom rule enforcement** based on your standards  
✅ **Actionable suggestions** with GitHub links  
✅ **Smart filtering** (only meaningful feedback)  
✅ **Context-aware analysis** (not just diff lines)  
✅ **Database storage** for review history  
✅ **API endpoints** for frontend integration  
✅ **Background processing** (webhooks don't wait)  

The AI agent will automatically review every PR that comes through your webhook, providing consistent, thorough code quality feedback based on your custom rules!
