"""
Main Review Generator that orchestrates the AI code review process
"""

import os
from typing import List, Optional, Dict, Any
from .config import AIConfig
from .models import CodeReviewSuggestion, CodeReviewResult, GitHubPRInfo, GitHubFileContent
from .github_client import GitHubClient
from .code_analyzer import CodeAnalyzer

class ReviewGenerator:
    """Main class for generating AI-powered code reviews"""
    
    def __init__(self):
        self.config = AIConfig()
        self.github_client = GitHubClient()
        self.code_analyzer = CodeAnalyzer()
    
    def generate_review(self, owner: str, repo: str, pr_number: int) -> Optional[CodeReviewResult]:
        """Generate complete code review for a pull request"""
        try:
            print(f"🔍 Starting AI code review for PR #{pr_number} in {owner}/{repo}")
            
            # Get PR information
            pr_info = self.github_client.get_pr_info(owner, repo, pr_number)
            if not pr_info:
                print("❌ Failed to get PR information")
                return None
            
            print(f"📁 Found {len(pr_info.files)} files to review")
            
            # Analyze each file
            all_suggestions = []
            files_reviewed = 0
            
            for file_diff in pr_info.files:
                try:
                    print(f"  📝 Analyzing {file_diff.filename}...")
                    
                    # Skip binary files or very large files
                    if self._should_skip_file(file_diff):
                        print(f"    ⏭️ Skipping {file_diff.filename} (binary or too large)")
                        continue
                    
                    # Get file content with context
                    file_content = self.github_client.get_file_diff_with_context(
                        owner, repo, file_diff.filename,
                        pr_info.head_sha, pr_info.base_sha,
                        self.config.CONTEXT_LINES
                    )
                    
                    if not file_content:
                        print(f"    ⚠️ Could not fetch content for {file_diff.filename}")
                        continue
                    
                    # Analyze the file
                    suggestions = self.code_analyzer.analyze_file(
                        file_content, pr_info.repository, pr_info.head_ref
                    )
                    
                    if suggestions:
                        print(f"    ✅ Found {len(suggestions)} suggestions")
                        all_suggestions.extend(suggestions)
                    else:
                        print(f"    ✅ No suggestions for {file_diff.filename}")
                    
                    files_reviewed += 1
                    
                except Exception as e:
                    print(f"    ❌ Error analyzing {file_diff.filename}: {e}")
                    continue
            
            # Generate review summary
            review_summary = self._generate_review_summary(all_suggestions, files_reviewed)
            
            # Create review result
            review_result = CodeReviewResult(
                pull_request_id=pr_number,  # This will be updated with actual DB ID
                suggestions=all_suggestions,
                total_suggestions=len(all_suggestions),
                files_reviewed=files_reviewed,
                review_summary=review_summary
            )
            
            print(f"🎉 Code review completed! Generated {len(all_suggestions)} suggestions")
            return review_result
            
        except Exception as e:
            print(f"❌ Error generating review: {e}")
            return None
    
    def _should_skip_file(self, file_diff: Any) -> bool:
        """Determine if a file should be skipped from analysis"""
        # Skip if file is too large
        if file_diff.changes > self.config.MAX_FILE_SIZE:
            return True
        
        # Skip binary files (common extensions)
        binary_extensions = {
            '.png', '.jpg', '.jpeg', '.gif', '.bmp', '.ico', '.svg',
            '.pdf', '.doc', '.docx', '.xls', '.xlsx',
            '.zip', '.tar', '.gz', '.rar', '.7z',
            '.exe', '.dll', '.so', '.dylib',
            '.mp3', '.mp4', '.avi', '.mov', '.wav'
        }
        
        filename = file_diff.filename.lower()
        return any(filename.endswith(ext) for ext in binary_extensions)
    
    def _generate_review_summary(self, suggestions: List[CodeReviewSuggestion], 
                               files_reviewed: int) -> str:
        """Generate a summary of the code review"""
        if not suggestions:
            return f"✅ Code review completed for {files_reviewed} files. No issues found - code quality is excellent!"
        
        # Count suggestions by severity
        severity_counts = {}
        type_counts = {}
        
        for suggestion in suggestions:
            severity = suggestion.severity.value
            suggestion_type = suggestion.suggestion_type.value
            
            severity_counts[severity] = severity_counts.get(severity, 0) + 1
            type_counts[suggestion_type] = type_counts.get(suggestion_type, 0) + 1
        
        # Build summary
        summary_parts = [f"Code review completed for {files_reviewed} files."]
        summary_parts.append(f"Found {len(suggestions)} suggestions for improvement:")
        
        # Add severity breakdown
        if severity_counts:
            severity_breakdown = ", ".join([f"{count} {severity}" for severity, count in severity_counts.items()])
            summary_parts.append(f"Severity: {severity_breakdown}")
        
        # Add type breakdown
        if type_counts:
            type_breakdown = ", ".join([f"{count} {suggestion_type}" for suggestion_type, count in type_counts.items()])
            summary_parts.append(f"Categories: {type_breakdown}")
        
        # Add recommendations
        if severity_counts.get('critical', 0) > 0:
            summary_parts.append("⚠️ Critical issues found - immediate attention required!")
        elif severity_counts.get('high', 0) > 0:
            summary_parts.append("🔴 High priority issues found - review and address soon.")
        else:
            summary_parts.append("✅ Overall code quality is good with minor improvements suggested.")
        
        return " ".join(summary_parts)
    
    def validate_configuration(self) -> bool:
        """Validate that all required configuration is present"""
        return self.config.validate()
