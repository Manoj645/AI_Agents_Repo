# AI Code Review Agent

An intelligent AI-powered code review system that automatically analyzes pull requests using custom rules and provides actionable suggestions for code quality improvements.

## 🚀 Features

- **AI-Powered Code Review**: Uses OpenAI GPT-4 to analyze code against custom rules
- **GitHub Integration**: Automatic webhook processing for PR events
- **Custom Rule Engine**: Enforce your team's coding standards automatically
- **PostgreSQL Database**: Store PR metadata and review suggestions
- **FastAPI Backend**: Modern, fast web framework with automatic API docs

## 🏗️ Architecture

```
GitHub Webhook → Store PR Data → AI Agent Analysis → Store Suggestions
     ↓              ↓              ↓              ↓
  webhooks.py   database.py   ai_agent/     code_reviews
                                    ↓
                              Custom Rules + OpenAI
```

## 🚀 Quick Start

1. **Clone and setup**:
   ```bash
   git clone <your-repo>
   cd AI_Agents_Repo/Api
   pip install -r requirements.txt
   ```

2. **Configure environment**:
   ```bash
   cp config.env.template config.env
   # Edit config.env with your API keys
   ```

3. **Run the application**:
   ```bash
   python3 -m uvicorn main:app --reload --host 127.0.0.1 --port 8000
   ```

4. **Access API docs**: http://localhost:8000/docs

## 📚 Documentation

- **API Documentation**: [Api/README.md](Api/README.md) - Detailed setup and API reference
- **AI Agent**: [Api/ai_agent/README.md](Api/ai_agent/README.md) - AI agent configuration and usage
- **Custom Rules**: [Custom-rules/python-code-standards.md](Custom-rules/python-code-standards.md) - Your coding standards

## 🔧 Configuration

Required environment variables in `config.env`:
- `OPENAI_API_KEY` - Your OpenAI API key
- `GITHUB_TOKEN` - GitHub personal access token
- `GITHUB_WEBHOOK_SECRET` - Webhook verification secret
- `DATABASE_URL` - PostgreSQL connection string

## 🎯 What It Does

1. **Monitors GitHub PRs** via webhooks
2. **Analyzes code changes** using AI against your custom rules
3. **Generates suggestions** for improvements, security, performance, etc.
4. **Stores results** in database for review history
5. **Provides API endpoints** for frontend integration

## 🧪 Testing

Test the AI agent with the provided test files in the `test files/` directory, which contain intentional code violations to verify the system works correctly.