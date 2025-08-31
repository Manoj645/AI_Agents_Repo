from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy import select, text
from sqlmodel import SQLModel
import traceback
from pydantic import ValidationError
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

@app.post("/webhooks/github")
async def github_webhook(request: Request, db: Session = Depends(get_db)):
    """Handle GitHub webhook events"""
    try:
        # Get request body
        body = await request.body()
        if not body:
            raise HTTPException(status_code=400, detail="Empty webhook payload")
        
        # Get headers
        headers = dict(request.headers)
        event_type = headers.get("X-GitHub-Event")
        signature = headers.get("X-Hub-Signature-256")
        
        if not event_type:
            raise HTTPException(status_code=400, detail="Missing X-GitHub-Event header")
        
        if not signature:
            raise HTTPException(status_code=400, detail="Missing X-Hub-Signature-256 header")
        
        # Verify signature and process webhook
        try:
            # Process webhook quickly to avoid timeout
            webhook_result = webhook_handler.handle_webhook(body, signature, event_type, db)
            
            # If webhook processing was successful and PR was stored, trigger AI review
            if webhook_result.get("success") and webhook_result.get("pr_id"):
                pr_id = webhook_result["pr_id"]
                print(f"🚀 Triggering AI review for PR ID: {pr_id}")
                
                # Trigger AI review asynchronously (don't wait for it to complete)
                try:
                    # Use asyncio.create_task to run in background
                    # This ensures webhook response is sent immediately
                    asyncio.create_task(ai_review_service.process_pr_review(db, pr_id))
                    print(f"✅ AI review task created for PR ID: {pr_id}")
                except Exception as ai_error:
                    print(f"⚠️ AI review trigger failed (non-blocking): {ai_error}")
                    # Don't fail the webhook if AI review fails
            else:
                print(f"ℹ️ No AI review triggered: {webhook_result.get('message', 'Unknown reason')}")
            
            # Return response immediately
            return webhook_result
            
        except Exception as webhook_error:
            raise HTTPException(
                status_code=500,
                detail=f"Webhook processing failed: {str(webhook_error)}"
            )
            
    except HTTPException:
        raise
    except Exception as e:
        error_details = {
            "status": "error",
            "message": "Webhook processing failed",
            "error": str(e),
            "error_type": type(e).__name__,
            "full_traceback": traceback.format_exc()
        }
        
        print(f"Webhook error: {error_details}")
        raise HTTPException(status_code=500, detail=error_details)

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
