# PR Review AI Agent - API

FastAPI application for AI-powered PR review with PostgreSQL database integration.

## 🚀 Quick Setup

### Prerequisites
- Python 3.9+
- PostgreSQL 14+

### Installation
```bash
# Install dependencies
pip3 install -r requirements.txt

# Setup database
createdb pr_review_db
python3 init_db.py

# Run the application
python3 -m uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

## 📚 API Documentation

- **Interactive Docs**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc

## 🔗 Key Endpoints

### Health & Status
- `GET /health` - Health check
- `GET /ai-config-test` - AI configuration status

### GitHub Integration
- `POST /webhooks/github` - GitHub webhook endpoint
- `GET /github-auth-test` - Test GitHub authentication

### AI Review
- `POST /trigger-ai-review/{pr_id}` - Manually trigger AI review
- `GET /check-reviews/{pr_id}` - Check existing reviews

### Database
- `GET /prs` - List all pull requests
- `GET /prs/{pr_id}` - Get specific PR details
- `GET /prs/{pr_id}/files` - Get files for a PR

## 🔧 Configuration

Copy `config.env.template` to `config.env` and fill in:
- `OPENAI_API_KEY` - OpenAI API key
- `GITHUB_TOKEN` - GitHub personal access token
- `GITHUB_WEBHOOK_SECRET` - Webhook verification secret
- `DATABASE_URL` - PostgreSQL connection string

## 🧪 Testing

Test the AI agent with:
```bash
# Test AI review
curl -X POST http://localhost:8000/trigger-ai-review/7

# Test GitHub auth
curl "http://localhost:8000/github-auth-test?token=YOUR_TOKEN&owner=YOUR_USERNAME&repo=YOUR_REPO&pr=14"
```

## 📁 Project Structure

- **`main.py`** - FastAPI application and endpoints
- **`ai_agent/`** - AI code review logic
- **`webhooks.py`** - GitHub webhook processing
- **`database.py`** - Database models and connection
- **`models.py`** - Data models
- **`requirements.txt`** - Python dependencies

For detailed AI agent documentation, see [ai_agent/README.md](ai_agent/README.md).
