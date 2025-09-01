from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy import select, text
from sqlmodel import SQLModel
import traceback
from pydantic import ValidationError
from typing import Optional
import json
import asyncio
from datetime import datetime

from database import get_db, create_db_and_tables
from models import PullRequest, File, CodeReview
from webhooks import GitHubWebhookHandler
from ai_agent.service import AIReviewService

app = FastAPI(title="PR Review AI Agent", version="1.0.0")

# Initialize webhook handler
webhook_handler = GitHubWebhookHandler()

# Initialize AI review service
ai_review_service = AIReviewService()

@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    create_db_and_tables()

@app.get("/")
async def root():
    """Root endpoint with available routes"""
    return {
        "message": "PR Review AI Agent API",
        "version": "1.0.0",
        "endpoints": [
            "/health",
            "/hello", 
            "/prs",
            "/prs/{pr_id}",
            "/prs/{pr_id}/files",
            "/prs/{pr_id}/suggestions",
            "/webhooks/github",
            "/db-test",
            "/ai-review/{pr_id}"
        ]
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "ok", "message": "Service is running"}

@app.get("/hello")
async def hello():
    """Simple hello endpoint"""
    return {"message": "Hello from PR Review AI Agent!"}

@app.get("/prs")
async def get_pull_requests(db: Session = Depends(get_db)):
    """Get all pull requests"""
    try:
        stmt = select(PullRequest).order_by(PullRequest.created_at.desc())
        prs = db.execute(stmt).scalars().all()
        
        return {
            "status": "success",
            "data": [
                {
                    "id": pr.id,
                    "title": pr.title,
                    "status": pr.status.value,
                    "author": pr.author,
                    "repository": pr.repository,
                    "pr_number": pr.pr_number,
                    "created_at": pr.created_at.isoformat(),
                    "html_url": pr.html_url
                }
                for pr in prs
            ]
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch pull requests: {str(e)}"
        )

@app.get("/prs/{pr_id}")
async def get_pull_request(pr_id: int, db: Session = Depends(get_db)):
    """Get a specific pull request by ID"""
    try:
        stmt = select(PullRequest).where(PullRequest.id == pr_id)
        pr = db.execute(stmt).scalar_one_or_none()
        
        if not pr:
            raise HTTPException(status_code=404, detail="Pull request not found")
        
        return {
            "status": "success",
            "data": {
                "id": pr.id,
                "title": pr.title,
                "description": pr.description,
                "status": pr.status.value,
                "author": pr.author,
                "repository": pr.repository,
                "pr_number": pr.pr_number,
                "github_id": pr.github_id,
                "html_url": pr.html_url,
                "branch_name": pr.branch_name,
                "base_branch": pr.base_branch,
                "additions": pr.additions,
                "deletions": pr.deletions,
                "changed_files": pr.changed_files,
                "created_at": pr.created_at.isoformat(),
                "updated_at": pr.updated_at.isoformat()
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch pull request: {str(e)}"
        )

@app.get("/prs/{pr_id}/files")
async def get_pr_files(pr_id: int, db: Session = Depends(get_db)):
    """Get files for a specific pull request"""
    try:
        stmt = select(File).where(File.pull_request_id == pr_id)
        files = db.execute(stmt).scalars().all()
        
        return {
            "status": "success",
            "data": [
                {
                    "id": file.id,
                    "filename": file.filename,
                    "status": file.status,
                    "additions": file.additions,
                    "deletions": file.deletions,
                    "changes": file.changes,
                    "file_size": file.file_size,
                    "file_extension": file.file_extension
                }
                for file in files
            ]
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch PR files: {str(e)}"
        )

@app.get("/prs/{pr_id}/suggestions")
async def get_pr_suggestions(pr_id: int, db: Session = Depends(get_db)):
    """Get AI review suggestions for a specific pull request"""
    try:
        suggestions = ai_review_service.get_pr_suggestions(db, pr_id)
        
        return {
            "status": "success",
            "data": {
                "pull_request_id": pr_id,
                "total_suggestions": len(suggestions),
                "suggestions": suggestions
            }
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch PR suggestions: {str(e)}"
        )

@app.post("/ai-review/{pr_id}")
async def trigger_ai_review(pr_id: int, db: Session = Depends(get_db)):
    """Manually trigger AI review for a pull request"""
    try:
        # Validate AI agent configuration
        if not ai_review_service.validate_configuration():
            raise HTTPException(
                status_code=500,
                detail="AI agent configuration is invalid. Please check environment variables."
            )
        
        # Process AI review
        result = await ai_review_service.process_pr_review(db, pr_id)
        
        if result["success"]:
            return {
                "status": "success",
                "message": result["message"],
                "data": result["data"]
            }
        else:
            raise HTTPException(
                status_code=500,
                detail=f"AI review failed: {result['error']}"
            )
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to trigger AI review: {str(e)}"
        )

@app.get("/webhook-test")
async def webhook_test():
    """Simple webhook test endpoint"""
    return {
        "status": "success",
        "message": "Webhook endpoint is accessible",
        "timestamp": datetime.now().isoformat(),
        "endpoint": "/webhooks/github",
        "method": "POST",
        "required_headers": [
            "X-GitHub-Event",
            "X-Hub-Signature-256"
        ]
    }

@app.post("/webhook-debug")
async def webhook_debug(request: Request):
    """Debug endpoint to test webhook headers and payload"""
    try:
        # Get request body
        body = await request.body()
        
        # Get all headers
        headers = dict(request.headers)
        
        # Log everything for debugging
        print("🔍 WEBHOOK DEBUG INFO:")
        print(f"📋 Method: {request.method}")
        print(f"📋 URL: {request.url}")
        print(f"📋 Headers: {headers}")
        print(f"📋 Body length: {len(body)} bytes")
        
        if body:
            try:
                body_text = body.decode('utf-8')
                print(f"📋 Body preview: {body_text[:200]}...")
            except:
                print("📋 Body: (not UTF-8 decodable)")
        
        # Check for GitHub-specific headers
        github_headers = {
            "X-GitHub-Event": headers.get("X-GitHub-Event"),
            "X-Hub-Signature-256": headers.get("X-Hub-Signature-256"),
            "User-Agent": headers.get("User-Agent"),
            "Content-Type": headers.get("Content-Type")
        }
        
        print(f"📋 GitHub headers: {github_headers}")
        
        return {
            "status": "success",
            "message": "Webhook debug info logged",
            "headers_received": list(headers.keys()),
            "github_headers": github_headers,
            "body_length": len(body)
        }
        
    except Exception as e:
        print(f"❌ Debug endpoint error: {e}")
        return {
            "status": "error",
            "message": str(e),
            "error_type": type(e).__name__
        }

@app.post("/webhooks/github")
async def github_webhook(request: Request, db: Session = Depends(get_db)):
    """Handle GitHub webhook events with enhanced debugging"""
    try:
        # Get request body
        body = await request.body()
        if not body:
            print("❌ Empty webhook payload received")
            return {"status": "error", "message": "Empty webhook payload"}
        
        # Get headers and log everything for debugging
        headers = dict(request.headers)
        print(f"🔍 WEBHOOK DEBUG - All headers: {headers}")
        
        # Try multiple ways to get event type
        event_type = headers.get("X-GitHub-Event") or headers.get("x-github-event") or headers.get("X-GITHUB-EVENT")
        
        print(f"🔍 Event type found: {event_type}")
        print(f"📦 Body length: {len(body)} bytes")
        
        # If no event type, try to infer from payload
        if not event_type:
            try:
                payload = json.loads(body.decode('utf-8'))
                if 'pull_request' in payload:
                    event_type = "pull_request"
                    print(f"🔍 Inferred event type from payload: {event_type}")
                elif 'ping' in payload:
                    event_type = "ping"
                    print(f"🔍 Inferred event type from payload: {event_type}")
            except:
                print("⚠️ Could not parse payload to infer event type")
        
        # Process webhook synchronously to ensure data is saved
        try:
            signature = headers.get("X-Hub-Signature-256", "no-signature")
            
            print(f"🔄 Processing webhook: {event_type}")
            webhook_result = webhook_handler.handle_webhook(body, signature, event_type, db)
            
            print(f"📊 Webhook result: {webhook_result}")
            
            # Trigger AI review if PR was created
            if webhook_result.get("success") and webhook_result.get("pr_id"):
                pr_id = webhook_result["pr_id"]
                print(f"🚀 Triggering AI review for PR ID: {pr_id}")
                
                # Trigger AI review asynchronously to avoid timeout
                try:
                    # Use asyncio.create_task for background processing
                    task = asyncio.create_task(ai_review_service.process_pr_review(db, pr_id))
                    
                    # Add callback to log completion/errors
                    def log_ai_result(task):
                        try:
                            result = task.result()
                            print(f"✅ AI review completed successfully for PR ID: {pr_id}")
                            print(f"📊 AI review result: {result}")
                        except Exception as e:
                            print(f"❌ AI review failed for PR ID: {pr_id}: {e}")
                            print(f"❌ AI error traceback: {traceback.format_exc()}")
                    
                    task.add_done_callback(log_ai_result)
                    print(f"✅ AI review task created for PR ID: {pr_id}")
                except Exception as ai_error:
                    print(f"❌ AI review task creation failed: {ai_error}")
                    print(f"❌ AI error traceback: {traceback.format_exc()}")
            
            return {
                "status": "success",
                "message": "Webhook processed successfully",
                "event_type": event_type,
                "pr_id": webhook_result.get("pr_id"),
                "result": webhook_result,
                "ai_review_triggered": webhook_result.get("success") and webhook_result.get("pr_id") is not None
            }
            
        except Exception as webhook_error:
            print(f"❌ Webhook processing error: {webhook_error}")
            print(f"❌ Error traceback: {traceback.format_exc()}")
            
            return {
                "status": "error",
                "message": f"Webhook processing failed: {str(webhook_error)}",
                "event_type": event_type
            }
            
    except Exception as e:
        print(f"❌ Webhook endpoint error: {e}")
        print(f"❌ Error traceback: {traceback.format_exc()}")
        return {
            "status": "error",
            "message": str(e)
        }

@app.get("/ai-config-test")
async def ai_config_test():
    """Test AI agent configuration"""
    try:
        from ai_agent.config import AIConfig
        
        config = AIConfig()
        
        # Check if config file exists
        import os
        config_file_exists = os.path.exists('config.env')
        
        # Check environment variables
        openai_key_set = bool(config.OPENAI_API_KEY and config.OPENAI_API_KEY != "your_openai_api_key_here")
        github_token_set = bool(config.GITHUB_TOKEN and config.GITHUB_TOKEN != "your_github_token_here")
        
        # Validate configuration
        is_valid = config.validate()
        
        return {
            "status": "success",
            "config_file_exists": config_file_exists,
            "openai_api_key_set": openai_key_set,
            "github_token_set": github_token_set,
            "configuration_valid": is_valid,
            "openai_model": config.OPENAI_MODEL,
            "max_tokens": config.MAX_TOKENS,
            "custom_rules_path": config.CUSTOM_RULES_PATH,
            "custom_rules_exists": os.path.exists(config.CUSTOM_RULES_PATH)
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }

@app.get("/github-auth-test")
async def github_auth_test(
    request: Request,
    owner: Optional[str] = None,
    repo: Optional[str] = None,
    pr: Optional[int] = None,
    token: Optional[str] = None,
):
    """Validate GitHub token and optionally check access to a specific PR.

    Usage:
    - /github-auth-test
    - /github-auth-test?owner=Manoj645&repo=AI_Agents_Repo&pr=14
    """
    try:
        from ai_agent.config import AIConfig
        import requests

        # Allow token from query param or headers; fall back to env
        # Preferred header: X-GitHub-Token; also support Authorization: token <TOKEN> or Bearer <TOKEN>
        hdrs = dict(request.headers)
        auth_hdr = hdrs.get("authorization") or hdrs.get("Authorization")
        header_token = hdrs.get("X-GitHub-Token") or hdrs.get("x-github-token")

        parsed_auth_token = None
        if auth_hdr:
            parts = auth_hdr.split()
            if len(parts) == 2 and parts[0].lower() in ("token", "bearer"):
                parsed_auth_token = parts[1]

        effective_token = token or header_token or parsed_auth_token or AIConfig.GITHUB_TOKEN

        headers = {
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "PR-Review-AI-Agent/1.0",
        }
        if effective_token:
            headers["Authorization"] = f"token {effective_token}"

        result = {
            "status": "success",
            "token_present": bool(effective_token and effective_token not in ("", "your_github_token_here")),
            "token_preview": (
                f"{effective_token[:4]}***{effective_token[-4:]}"
                if effective_token and len(effective_token) >= 10 else None
            ),
            "token_source": (
                "query_param" if token else (
                    "header" if (header_token or parsed_auth_token) else "env"
                )
            ),
        }

        # Basic auth test against /user
        try:
            resp = requests.get("https://api.github.com/user", headers=headers, timeout=10)
            result["user_status"] = resp.status_code
            if resp.ok:
                data = resp.json()
                result["user_login"] = data.get("login")
            else:
                result["user_error"] = resp.text[:200]
        except Exception as e:
            result["user_exception"] = str(e)

        # Optional PR check
        if owner and repo and pr is not None:
            pr_url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr}"
            try:
                pr_resp = requests.get(pr_url, headers=headers, timeout=10)
                result["pr_status"] = pr_resp.status_code
                result["pr_url"] = pr_url
                if pr_resp.ok:
                    pr_json = pr_resp.json()
                    result["pr_title"] = pr_json.get("title")
                else:
                    result["pr_error"] = pr_resp.text[:300]
            except Exception as e:
                result["pr_exception"] = str(e)

        return result

    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/openai-test")
async def openai_test():
    """Test OpenAI API key and connection"""
    try:
        import os
        from ai_agent.config import AIConfig
        import openai
        
        config = AIConfig()
        
        if not config.OPENAI_API_KEY or config.OPENAI_API_KEY == "your_openai_api_key_here":
            return {
                "status": "error",
                "message": "OpenAI API key not set",
                "key_present": False
            }
        
        # Test the API key
        try:
            client = openai.OpenAI(api_key=config.OPENAI_API_KEY)
            
            # Test with a simple completion using the configured model
            response = client.chat.completions.create(
                model=config.OPENAI_MODEL,
                messages=[{"role": "user", "content": "Hello"}],
                max_tokens=5
            )
            
            return {
                "status": "success",
                "message": "OpenAI API key is valid",
                "key_present": True,
                "key_preview": f"{config.OPENAI_API_KEY[:7]}***{config.OPENAI_API_KEY[-4:]}",
                "model_used": config.OPENAI_MODEL,
                "model_source": "environment" if os.getenv("OPENAI_MODEL") else "default",
                "test_response": response.choices[0].message.content,
                "available_models": [
                    "gpt-4o",           # Best quality, moderate cost
                    "gpt-4o-mini",      # Good quality, very cheap
                    "gpt-4-turbo",      # Good quality, moderate cost
                    "gpt-3.5-turbo",    # Fast, very cheap
                    "gpt-3.5-turbo-16k" # Fast, cheap, longer context
                ],
                "model_info": {
                    "gpt-4o": "Best overall performance, 128K context, ~$0.01/$0.03 per 1K tokens",
                    "gpt-4o-mini": "Great quality, 128K context, ~$0.00015/$0.0006 per 1K tokens",
                    "gpt-4-turbo": "Good quality, 128K context, ~$0.01/$0.03 per 1K tokens",
                    "gpt-3.5-turbo": "Fast & cheap, 16K context, ~$0.0005/$0.0015 per 1K tokens",
                    "gpt-3.5-turbo-16k": "Fast & cheap, 16K context, ~$0.003/$0.004 per 1K tokens"
                }
            }
            
        except Exception as api_error:
            return {
                "status": "error",
                "message": f"OpenAI API error: {str(api_error)}",
                "key_present": True,
                "key_preview": f"{config.OPENAI_API_KEY[:7]}***{config.OPENAI_API_KEY[-4:]}",
                "model_used": config.OPENAI_MODEL,
                "model_source": "environment" if os.getenv("OPENAI_MODEL") else "default",
                "error_type": type(api_error).__name__,
                "available_models": [
                    "gpt-4o", "gpt-4o-mini", "gpt-4-turbo", "gpt-3.5-turbo", "gpt-3.5-turbo-16k"
                ]
            }
            
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }

@app.get("/check-reviews/{pr_id}")
async def check_reviews(pr_id: int, db: Session = Depends(get_db)):
    """Check if code reviews exist for a specific PR"""
    try:
        from sqlalchemy import select
        from models import PullRequest, CodeReview
        
        # Check if PR exists
        pr_stmt = select(PullRequest).where(PullRequest.id == pr_id)
        pr = db.execute(pr_stmt).scalar_one_or_none()
        
        if not pr:
            return {
                "status": "error",
                "message": f"PR with ID {pr_id} not found"
            }
        
        # Check for code reviews
        review_stmt = select(CodeReview).where(CodeReview.pull_request_id == pr_id)
        reviews = db.execute(review_stmt).scalars().all()
        
        return {
            "status": "success",
            "pr_id": pr_id,
            "pr_number": pr.pr_number,
            "pr_title": pr.title,
            "reviews_count": len(reviews),
            "reviews": [
                {
                    "id": review.id,
                    "suggestion_type": review.suggestion_type,
                    "severity": review.severity,
                    "message": review.message,
                    "line_number": review.line_number,
                    "created_at": review.created_at.isoformat() if review.created_at else None
                }
                for review in reviews
            ]
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }

@app.post("/trigger-ai-review/{pr_id}")
async def trigger_ai_review(pr_id: int, db: Session = Depends(get_db)):
    """Manually trigger AI review for a specific PR"""
    try:
        print(f"🚀 Manually triggering AI review for PR ID: {pr_id}")
        
        # Check if PR exists
        from sqlalchemy import select
        from models import PullRequest
        
        stmt = select(PullRequest).where(PullRequest.id == pr_id)
        pr = db.execute(stmt).scalar_one_or_none()
        
        if not pr:
            return {
                "status": "error",
                "message": f"PR with ID {pr_id} not found"
            }
        
        print(f"📋 Found PR: #{pr.pr_number} - {pr.title}")
        
        # Trigger AI review
        try:
            ai_result = await ai_review_service.process_pr_review(db, pr_id)
            return {
                "status": "success",
                "message": "AI review completed",
                "pr_id": pr_id,
                "pr_number": pr.pr_number,
                "result": ai_result
            }
        except Exception as ai_error:
            print(f"❌ AI review failed: {ai_error}")
            print(f"❌ AI error traceback: {traceback.format_exc()}")
            return {
                "status": "error",
                "message": f"AI review failed: {str(ai_error)}",
                "pr_id": pr_id,
                "error_traceback": traceback.format_exc()
            }
            
    except Exception as e:
        print(f"❌ Manual AI review trigger failed: {e}")
        return {
            "status": "error",
            "message": str(e)
        }

@app.get("/db-test")
async def database_connection_test(db: Session = Depends(get_db)):
    """Test database connection and basic operations"""
    try:
        # Test 1: Basic connection
        db.execute(text("SELECT 1"))
        
        # Test 2: Check if tables exist
        result = db.execute(text("SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'public'"))
        table_count = result.scalar()
        
        # Test 3: Check if our specific tables exist
        pr_table_exists = db.execute(text("SELECT EXISTS(SELECT 1 FROM information_schema.tables WHERE table_name = 'pull_requests')")).scalar()
        files_table_exists = db.execute(text("SELECT EXISTS(SELECT 1 FROM information_schema.tables WHERE table_name = 'files')")).scalar()
        reviews_table_exists = db.execute(text("SELECT EXISTS(SELECT 1 FROM information_schema.tables WHERE table_name = 'code_reviews')")).scalar()
        
        # Test 4: Try to count records (should work even if tables are empty)
        pr_count = db.execute(text("SELECT COUNT(*) FROM pull_requests")).scalar() if pr_table_exists else 0
        files_count = db.execute(text("SELECT COUNT(*) FROM files")).scalar() if files_table_exists else 0
        reviews_count = db.execute(text("SELECT COUNT(*) FROM code_reviews")).scalar() if reviews_table_exists else 0
        
        return {
            "status": "success",
            "message": "Database connection test passed",
            "details": {
                "connection": "OK",
                "total_tables": table_count,
                "pull_requests_table": pr_table_exists,
                "files_table": files_table_exists,
                "code_reviews_table": reviews_table_exists,
                "pull_requests_count": pr_count,
                "files_count": files_count,
                "code_reviews_count": reviews_count
            }
        }
        
    except Exception as e:
        error_details = {
            "status": "error",
            "message": "Database connection test failed",
            "error": str(e),
            "error_type": type(e).__name__,
            "error_details": {
                "full_traceback": traceback.format_exc(),
                "suggestion": _get_error_suggestion(e)
            }
        }
        
        # Log the full error for debugging
        print(f"Database test error: {error_details}")
        return error_details

def _get_error_suggestion(error: Exception) -> str:
    """Get helpful suggestions based on error type"""
    error_type = type(error).__name__
    
    if "connection" in str(error).lower():
        return "Check if the database is running and accessible. Verify DATABASE_URL in config.env"
    elif "authentication" in str(error).lower() or "password" in str(error).lower():
        return "Check database credentials in DATABASE_URL. Verify username and password"
    elif "does not exist" in str(error).lower():
        return "Database or table does not exist. Run init_db.py to create tables"
    elif "permission" in str(error).lower():
        return "Database user lacks permissions. Check user privileges"
    elif "timeout" in str(error).lower():
        return "Database connection timeout. Check network connectivity and database load"
    else:
        return "Check database configuration and ensure all required packages are installed"

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
