"""
GitHub API client for fetching PR information and code diffs
"""

import requests
import base64
import re
from typing import List, Optional, Dict, Any
from .config import AIConfig
from .models import GitHubFileDiff, GitHubFileContent, GitHubPRInfo

class GitHubClient:
    """GitHub API client for code review"""
    
    def __init__(self):
        self.config = AIConfig()
        self.headers = self.config.get_github_headers()
        self.base_url = self.config.GITHUB_API_BASE
    
    def get_pr_info(self, owner: str, repo: str, pr_number: int) -> Optional[GitHubPRInfo]:
        """Get PR information including files changed"""
        try:
            # Get PR details
            pr_url = f"{self.base_url}/repos/{owner}/{repo}/pulls/{pr_number}"
            pr_response = requests.get(pr_url, headers=self.headers, timeout=30)
            pr_response.raise_for_status()
            pr_data = pr_response.json()
            
            # Get files changed
            files_url = f"{self.base_url}/repos/{owner}/{repo}/pulls/{pr_number}/files"
            files_response = requests.get(files_url, headers=self.headers, timeout=30)
            files_response.raise_for_status()
            files_data = files_response.json()
            
            # Parse files
            files = []
            for file_data in files_data:
                file_diff = GitHubFileDiff(
                    filename=file_data["filename"],
                    status=file_data["status"],
                    additions=file_data["additions"],
                    deletions=file_data["deletions"],
                    changes=file_data["changes"],
                    patch=file_data.get("patch"),
                    blob_url=file_data["blob_url"],
                    raw_url=file_data["raw_url"],
                    contents_url=file_data["contents_url"]
                )
                files.append(file_diff)
            
            # Create PR info
            pr_info = GitHubPRInfo(
                number=pr_data["number"],
                title=pr_data["title"],
                body=pr_data.get("body"),
                head_sha=pr_data["head"]["sha"],
                base_sha=pr_data["base"]["sha"],
                head_ref=pr_data["head"]["ref"],
                base_ref=pr_data["base"]["ref"],
                repository=f"{owner}/{repo}",
                files=files
            )
            
            return pr_info
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Error fetching PR info: {e}")
            return None
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            return None
    
    def get_file_content(self, owner: str, repo: str, file_path: str, ref: str) -> Optional[GitHubFileContent]:
        """Get file content from GitHub"""
        try:
            url = f"{self.base_url}/repos/{owner}/{repo}/contents/{file_path}"
            params = {"ref": ref}
            
            response = requests.get(url, headers=self.headers, params=params, timeout=30)
            response.raise_for_status()
            file_data = response.json()
            
            # Decode content
            if file_data["encoding"] == "base64":
                content = base64.b64decode(file_data["content"]).decode("utf-8")
            else:
                content = file_data["content"]
            
            file_content = GitHubFileContent(
                filename=file_data["name"],
                content=content,
                encoding=file_data["encoding"],
                size=file_data["size"],
                sha=file_data["sha"],
                url=file_data["url"],
                git_url=file_data["git_url"],
                html_url=file_data["html_url"],
                download_url=file_data["download_url"]
            )
            
            return file_content
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Error fetching file content for {file_path}: {e}")
            return None
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            return None
    
    def get_file_diff_with_context(self, owner: str, repo: str, file_path: str, 
                                 head_sha: str, base_sha: str, 
                                 context_lines: int = 5) -> Optional[GitHubFileContent]:
        """Get file content with diff context for better analysis"""
        try:
            # Get head version (new version)
            head_content = self.get_file_content(owner, repo, file_path, head_sha)
            if not head_content:
                return None
            
            # Get base version (old version) for comparison
            base_content = self.get_file_content(owner, repo, file_path, base_sha)
            
            # Parse diff to get changed lines
            if base_content:
                diff_lines = self._parse_diff_lines(head_content.content, base_content.content)
                head_content.diff_lines = diff_lines
            
            # Add context lines around changes
            if head_content.diff_lines:
                head_content.context_lines = self._get_context_lines(
                    head_content.content, head_content.diff_lines, context_lines
                )
            
            return head_content
            
        except Exception as e:
            print(f"❌ Error getting file diff with context: {e}")
            return None
    
    def _parse_diff_lines(self, new_content: str, old_content: str) -> List[str]:
        """Parse diff to identify changed lines (simplified)"""
        new_lines = new_content.split('\n')
        old_lines = old_content.split('\n')
        
        changed_lines = []
        for i, (new_line, old_line) in enumerate(zip(new_lines, old_lines)):
            if new_line != old_line:
                changed_lines.append(f"Line {i+1}: {new_line}")
        
        return changed_lines
    
    def _get_context_lines(self, content: str, diff_lines: List[str], context_lines: int) -> List[str]:
        """Get context lines around changes"""
        lines = content.split('\n')
        context_lines_list = []
        
        for diff_line in diff_lines:
            # Extract line number from diff line
            match = re.search(r'Line (\d+):', diff_line)
            if match:
                line_num = int(match.group(1)) - 1  # Convert to 0-based index
                
                # Get context before
                start = max(0, line_num - context_lines)
                end = min(len(lines), line_num + context_lines + 1)
                
                for i in range(start, end):
                    prefix = ">>> " if i == line_num else "    "
                    context_lines_list.append(f"{prefix}Line {i+1}: {lines[i]}")
                
                context_lines_list.append("---")  # Separator
        
        return context_lines_list
    
    def generate_github_url(self, owner: str, repo: str, file_path: str, 
                           line_number: Optional[int] = None, ref: str = "main") -> str:
        """Generate GitHub URL for specific file and line"""
        base_url = f"https://github.com/{owner}/{repo}/blob/{ref}/{file_path}"
        if line_number:
            return f"{base_url}#L{line_number}"
        return base_url
