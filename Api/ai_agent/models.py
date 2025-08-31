"""
Data models for the AI Code Review Agent
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum

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

class CodeReviewSuggestion(BaseModel):
    """A single code review suggestion"""
    file_path: str
    line_number: Optional[int] = None
    suggestion_type: SuggestionType
    severity: Severity = Severity.MEDIUM
    title: str
    description: str
    suggestion: Optional[str] = None
    github_url: Optional[str] = None
    rule_applied: Optional[str] = None
    context_lines: Optional[List[str]] = None

class GitHubFileDiff(BaseModel):
    """GitHub file diff information"""
    filename: str
    status: str
    additions: int
    deletions: int
    changes: int
    patch: Optional[str] = None
    blob_url: str
    raw_url: str
    contents_url: str

class GitHubPRInfo(BaseModel):
    """GitHub PR information for analysis"""
    number: int
    title: str
    body: Optional[str] = None
    head_sha: str
    base_sha: str
    head_ref: str
    base_ref: str
    repository: str
    files: List[GitHubFileDiff]

class CodeReviewResult(BaseModel):
    """Complete code review result for a PR"""
    pull_request_id: int
    suggestions: List[CodeReviewSuggestion]
    total_suggestions: int
    files_reviewed: int
    review_summary: str
    created_at: datetime = Field(default_factory=datetime.now)

class GitHubFileContent(BaseModel):
    """GitHub file content with context"""
    filename: str
    content: str
    encoding: str
    size: int
    sha: str
    url: str
    git_url: str
    html_url: str
    download_url: str
    context_lines: List[str] = Field(default_factory=list)
    diff_lines: List[str] = Field(default_factory=list)
