# AI Code Review Agent

AI-powered code review functionality using LangChain and OpenAI to automatically analyze pull requests and generate code quality suggestions.

## 🚀 Quick Start

### 1. Environment Setup
Add to your `config.env`:
```bash
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4o
GITHUB_TOKEN=your_github_token_here
```

### 2. Usage
The AI agent runs automatically when GitHub webhooks are received, or manually via:
```bash
POST /trigger-ai-review/{pr_id}
```

## 🏗️ Architecture

```
GitHub Webhook → Store PR Data → AI Agent → Analyze Code → Store Suggestions
     ↓              ↓              ↓           ↓           ↓
  webhooks.py   database.py   ai_agent/    LangChain   code_reviews
                                    ↓
                              GitHub API (fetch diffs + context)
```

## 📁 Core Components

- **`config.py`** - Configuration and environment variables
- **`models.py`** - Data models for suggestions and GitHub responses
- **`github_client.py`** - GitHub API client for fetching PR data
- **`code_analyzer.py`** - Core AI agent using LangChain + OpenAI
- **`review_generator.py`** - Main orchestrator for review process
- **`service.py`** - Service layer for database integration

## 🎯 How It Works

1. **GitHub Integration**: Fetches PR diffs and file contents
2. **Context Analysis**: Analyzes changed lines with surrounding context
3. **AI Review**: Uses OpenAI to analyze code against custom rules
4. **Smart Filtering**: Only stores meaningful suggestions
5. **Database Storage**: Stores suggestions with GitHub links

## 🔧 Configuration Options

- **`CONTEXT_LINES`**: Lines before/after diff for context (default: 5)
- **`MAX_FILE_SIZE`**: Maximum file size to analyze (default: 1MB)
- **`TEMPERATURE`**: AI creativity level (default: 0.1)
- **`MAX_TOKENS`**: Maximum tokens for AI response (default: 4000)

## 📝 Output Format

Each suggestion includes:
- **File path** and **line number**
- **Suggestion type** (improvement, bug, style, security, etc.)
- **Severity level** (low, medium, high, critical)
- **Title**, **description**, and **specific suggestion**
- **GitHub URL** linking directly to relevant line
- **Rule applied** from your custom standards

## 🧪 Testing

Test the AI agent:
```bash
# Test configuration
python -c "from ai_agent.config import AIConfig; print(AIConfig.validate())"

# Test components
python -c "from ai_agent.github_client import GitHubClient; print('GitHub client ready')"
python -c "from ai_agent.code_analyzer import CodeAnalyzer; print('Code analyzer ready')"
```

## 🎉 What You Get

✅ **Automatic code reviews** on every PR  
✅ **Custom rule enforcement** based on your standards  
✅ **Actionable suggestions** with GitHub links  
✅ **Smart filtering** (only meaningful feedback)  
✅ **Context-aware analysis** (not just diff lines)  
✅ **Database storage** for review history  

The AI agent automatically reviews every PR through your webhook, providing consistent, thorough code quality feedback based on your custom rules!
