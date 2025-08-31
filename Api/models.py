from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime, timezone
from enum import Enum

class PRStatus(str, Enum):
    OPEN = "open"
    CLOSED = "closed"
    MERGED = "merged"

class SuggestionType(str, Enum):
    """Types of code review suggestions"""
    IMPROVEMENT = "improvement"
    BUG = "bug"
    STYLE = "style"
    SECURITY = "security"
    PERFORMANCE = "performance"
    DOCUMENTATION = "documentation"
    TESTING = "testing"

class Severity(str, Enum):
    """Severity levels for suggestions"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class PullRequest(SQLModel, table=True):
    """Pull Request model"""
    __tablename__ = "pull_requests"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(max_length=255)
    description: Optional[str] = Field(default=None)
    status: PRStatus = Field(default=PRStatus.OPEN)
    author: str = Field(max_length=100)
    repository: str = Field(max_length=255)
    pr_number: int = Field(unique=True)
    github_id: Optional[int] = Field(default=None) # This will map to BIGINT in DB
    html_url: Optional[str] = Field(default=None, max_length=500)
    
    # Enhanced metadata fields
    branch_name: Optional[str] = Field(default=None, max_length=100)
    base_branch: Optional[str] = Field(default=None, max_length=100)
    commit_sha: Optional[str] = Field(default=None, max_length=40)
    base_commit_sha: Optional[str] = Field(default=None, max_length=40)
    
    # Code diff statistics
    additions: Optional[int] = Field(default=0)
    deletions: Optional[int] = Field(default=0)
    changed_files: Optional[int] = Field(default=0)
    commits_count: Optional[int] = Field(default=0)
    
    # GitHub specific fields
    draft: Optional[bool] = Field(default=False)
    mergeable: Optional[bool] = Field(default=None)
    rebaseable: Optional[bool] = Field(default=None)
    mergeable_state: Optional[str] = Field(default=None, max_length=50)
    
    # Timestamps
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    closed_at: Optional[datetime] = Field(default=None)
    merged_at: Optional[datetime] = Field(default=None)
    
    # Relationships
    files: List["File"] = Relationship(back_populates="pull_request")
    code_reviews: List["CodeReview"] = Relationship(back_populates="pull_request")

class File(SQLModel, table=True):
    """File model"""
    __tablename__ = "files"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    filename: str = Field(max_length=255)
    status: str = Field(max_length=50)
    additions: int = Field(default=0)
    deletions: int = Field(default=0)
    changes: int = Field(default=0)
    patch: Optional[str] = Field(default=None)
    
    # Enhanced metadata fields
    sha: Optional[str] = Field(default=None, max_length=40)
    blob_url: Optional[str] = Field(default=None, max_length=500)
    raw_url: Optional[str] = Field(default=None, max_length=500)
    contents_url: Optional[str] = Field(default=None, max_length=500)
    file_size: Optional[int] = Field(default=None)
    file_extension: Optional[str] = Field(default=None, max_length=20)
    
    # Foreign key
    pull_request_id: int = Field(foreign_key="pull_requests.id")
    pull_request: Optional[PullRequest] = Relationship(back_populates="files")

class CodeReview(SQLModel, table=True):
    """Code Review model for AI-generated suggestions"""
    __tablename__ = "code_reviews"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    pull_request_id: int = Field(foreign_key="pull_requests.id")
    file_path: str = Field(max_length=500)
    line_number: Optional[int] = Field(default=None)
    suggestion_type: SuggestionType
    severity: Severity = Field(default=Severity.MEDIUM)
    title: str = Field(max_length=255)
    description: str
    suggestion: Optional[str] = Field(default=None)
    github_url: Optional[str] = Field(default=None, max_length=500)
    rule_applied: Optional[str] = Field(default=None, max_length=100)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
    # Relationship
    pull_request: Optional[PullRequest] = Relationship(back_populates="code_reviews")
