"""
Service layer for integrating AI agent with database and webhook system
"""

import asyncio
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import select
from models import PullRequest, CodeReview
from ai_agent.review_generator import ReviewGenerator
from ai_agent.config import AIConfig

class AIReviewService:
    """Service for managing AI code reviews"""
    
    def __init__(self):
        self.review_generator = ReviewGenerator()
    
    async def process_pr_review(self, db: Session, pr_id: int) -> Dict[str, Any]:
        """Process AI review for a pull request and store results in database"""
        try:
            print(f"🤖 Starting AI review process for PR ID: {pr_id}")
            
            # Validate configuration first
            if not self.config.validate():
                return {
                    "success": False, 
                    "error": "AI Agent configuration is invalid. Please check OPENAI_API_KEY and GITHUB_TOKEN in config.env"
                }
            
            # Get PR information from database
            stmt = select(PullRequest).where(PullRequest.id == pr_id)
            pr = db.execute(stmt).scalar_one_or_none()
            if not pr:
                return {"success": False, "error": f"Pull request with ID {pr_id} not found"}
            
            # Extract repository info from PR data
            repo_parts = pr.repository.split('/')
            if len(repo_parts) != 2:
                return {"success": False, "error": f"Invalid repository format: {pr.repository}"}
            
            owner, repo_name = repo_parts
            
            print(f"🔍 Fetching PR #{pr.pr_number} from {owner}/{repo_name}")
            
            # Generate AI review
            review_result = self.review_generator.generate_review(owner, repo_name, pr.pr_number)
            if not review_result:
                return {"success": False, "error": "Failed to generate AI review - check logs for details"}
            
            # Store suggestions in database (only if there are meaningful suggestions)
            if review_result.suggestions:
                stored_suggestions = await self._store_suggestions(db, pr_id, review_result.suggestions)
                
                return {
                    "success": True,
                    "message": "AI review completed and suggestions stored",
                    "data": {
                        "total_suggestions": len(stored_suggestions),
                        "files_reviewed": review_result.files_reviewed,
                        "review_summary": review_result.review_summary,
                        "suggestions": [
                            {
                                "id": s.id,
                                "file_path": s.file_path,
                                "line_number": s.line_number,
                                "suggestion_type": s.suggestion_type.value,
                                "severity": s.severity.value,
                                "title": s.title,
                                "description": s.description,
                                "suggestion": s.suggestion,
                                "github_url": s.github_url,
                                "rule_applied": s.rule_applied
                            }
                            for s in stored_suggestions
                        ]
                    }
                }
            else:
                return {
                    "success": True,
                    "message": "AI review completed - no suggestions found (code quality is good)",
                    "data": {
                        "total_suggestions": 0,
                        "files_reviewed": review_result.files_reviewed,
                        "review_summary": review_result.review_summary
                    }
                }
                
        except Exception as e:
            print(f"❌ Error in AI review service: {e}")
            return {"success": False, "error": str(e)}
    
    async def _store_suggestions(self, db: Session, pr_id: int, 
                               suggestions: List[Any]) -> List[CodeReview]:
        """Store AI review suggestions in database"""
        stored_suggestions = []
        
        try:
            for suggestion in suggestions:
                # Create CodeReview record
                code_review = CodeReview(
                    pull_request_id=pr_id,
                    file_path=suggestion.file_path,
                    line_number=suggestion.line_number,
                    suggestion_type=suggestion.suggestion_type.value,
                    severity=suggestion.severity.value,
                    title=suggestion.title,
                    description=suggestion.description,
                    suggestion=suggestion.suggestion,
                    github_url=suggestion.github_url,
                    rule_applied=suggestion.rule_applied
                )
                
                # Add to database
                db.add(code_review)
                db.commit()
                db.refresh(code_review)
                
                stored_suggestions.append(code_review)
            
            print(f"✅ Stored {len(stored_suggestions)} suggestions in database")
            return stored_suggestions
            
        except Exception as e:
            print(f"❌ Error storing suggestions: {e}")
            db.rollback()
            raise
    
    def get_pr_suggestions(self, db: Session, pr_id: int) -> List[Dict[str, Any]]:
        """Get all AI review suggestions for a pull request"""
        try:
            stmt = select(CodeReview).where(CodeReview.pull_request_id == pr_id)
            suggestions = db.execute(stmt).scalars().all()
            
            return [
                {
                    "id": s.id,
                    "file_path": s.file_path,
                    "line_number": s.line_number,
                    "suggestion_type": s.suggestion_type.value,
                    "severity": s.severity.value,
                    "title": s.title,
                    "description": s.description,
                    "suggestion": s.suggestion,
                    "github_url": s.github_url,
                    "rule_applied": s.rule_applied,
                    "created_at": s.created_at.isoformat()
                }
                for s in suggestions
            ]
            
        except Exception as e:
            print(f"❌ Error fetching suggestions: {e}")
            return []
    
    def validate_configuration(self) -> bool:
        """Validate AI agent configuration"""
        return self.review_generator.validate_configuration()
