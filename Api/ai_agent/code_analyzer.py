"""
AI Code Analyzer using LangChain and OpenAI
"""

import os
from typing import List, Optional, Dict, Any
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import HumanMessage, SystemMessage
from .config import AIConfig
from .models import CodeReviewSuggestion, SuggestionType, Severity, GitHubFileContent

class CodeAnalyzer:
    """AI-powered code analyzer using LangChain"""
    
    def __init__(self):
        self.config = AIConfig()
        self.llm = ChatOpenAI(
            model=self.config.OPENAI_MODEL,
            temperature=self.config.TEMPERATURE,
            max_tokens=self.config.MAX_TOKENS,
            api_key=self.config.OPENAI_API_KEY
        )
        self.custom_rules = self._load_custom_rules()
    
    def _load_custom_rules(self) -> str:
        """Load custom code review rules from markdown file"""
        try:
            rules_path = self.config.CUSTOM_RULES_PATH
            if os.path.exists(rules_path):
                with open(rules_path, 'r', encoding='utf-8') as f:
                    return f.read()
            else:
                print(f"⚠️ Custom rules file not found: {rules_path}")
                return self._get_default_rules()
        except Exception as e:
            print(f"⚠️ Error loading custom rules: {e}")
            return self._get_default_rules()
    
    def _get_default_rules(self) -> str:
        """Fallback default rules if custom file not found"""
        return """
        # Python Code Standards for AI Code Review
        
        ## Code Quality Rules:
        1. Functions should not exceed 15 lines
        2. Use descriptive variable names (snake_case)
        3. Add proper error handling with try-except
        4. Include comprehensive docstrings
        5. Avoid magic numbers, use constants
        6. Follow PEP 8 formatting guidelines
        7. Use type hints where appropriate
        8. Write testable code
        9. Consider performance implications
        10. Ensure code readability
        """
    
    def analyze_file(self, file_content: GitHubFileContent, 
                    repository: str, branch: str) -> List[CodeReviewSuggestion]:
        """Analyze a single file and generate review suggestions"""
        try:
            # Prepare analysis prompt
            analysis_prompt = self._create_analysis_prompt(file_content, repository, branch)
            
            # Get AI analysis
            response = self.llm.invoke([
                SystemMessage(content="You are an expert Python code reviewer. Analyze the code and provide specific, actionable suggestions."),
                HumanMessage(content=analysis_prompt)
            ])
            
            # Parse suggestions
            suggestions = self._parse_ai_response(response.content, file_content, repository, branch)
            
            return suggestions
            
        except Exception as e:
            print(f"❌ Error analyzing file {file_content.filename}: {e}")
            return []
    
    def _create_analysis_prompt(self, file_content: GitHubFileContent, 
                               repository: str, branch: str) -> str:
        """Create the analysis prompt for the AI"""
        
        # Build context information
        context_info = ""
        if file_content.context_lines:
            context_info = "\n\n## Context Around Changes:\n" + "\n".join(file_content.context_lines)
        
        diff_info = ""
        if file_content.diff_lines:
            diff_info = "\n\n## Changed Lines:\n" + "\n".join(file_content.diff_lines)
        
        prompt = f"""
        # Code Review Analysis Request
        
        ## Repository: {repository}
        ## Branch: {branch}
        ## File: {file_content.filename}
        ## File Size: {file_content.size} bytes
        
        ## Custom Code Review Rules:
        {self.custom_rules}
        
        ## File Content:
        ```{self._get_file_extension(file_content.filename)}
        {file_content.content}
        ```
        
        {context_info}
        {diff_info}
        
        ## Analysis Instructions:
        1. Review the code against the custom rules above
        2. Focus on the changed lines and their context
        3. Provide specific, actionable suggestions
        4. Include line numbers where applicable
        5. Categorize suggestions by type and severity
        6. Only provide suggestions if there are actual issues to address
        
        ## Response Format:
        For each suggestion, provide:
        - Type: improvement/bug/style/security/performance/documentation/testing
        - Severity: low/medium/high/critical
        - Title: Short descriptive title
        - Description: Detailed explanation of the issue
        - Suggestion: Specific recommendation for improvement
        - Line Number: The specific line(s) affected
        
        If the code looks good and follows all rules, respond with: "CODE_QUALITY_GOOD"
        """
        
        return prompt
    
    def _get_file_extension(self, filename: str) -> str:
        """Get file extension for syntax highlighting"""
        if '.' in filename:
            return filename.split('.')[-1]
        return 'text'
    
    def _parse_ai_response(self, response: str, file_content: GitHubFileContent,
                          repository: str, branch: str) -> List[CodeReviewSuggestion]:
        """Parse AI response into structured suggestions"""
        suggestions = []
        
        # Check if code quality is good
        if "CODE_QUALITY_GOOD" in response.upper():
            return []
        
        # Parse suggestions (this is a simplified parser - you might want to enhance it)
        lines = response.split('\n')
        current_suggestion = {}
        
        for line in lines:
            line = line.strip()
            
            # Look for suggestion patterns
            if line.startswith('- Type:') or line.startswith('Type:'):
                if current_suggestion and 'type' in current_suggestion:
                    # Save previous suggestion
                    suggestion = self._create_suggestion_from_dict(current_suggestion, file_content, repository, branch)
                    if suggestion:
                        suggestions.append(suggestion)
                
                # Start new suggestion
                current_suggestion = {'type': line.split(':', 1)[1].strip()}
                
            elif line.startswith('- Severity:') or line.startswith('Severity:'):
                current_suggestion['severity'] = line.split(':', 1)[1].strip()
            elif line.startswith('- Title:') or line.startswith('Title:'):
                current_suggestion['title'] = line.split(':', 1)[1].strip()
            elif line.startswith('- Description:') or line.startswith('Description:'):
                current_suggestion['description'] = line.split(':', 1)[1].strip()
            elif line.startswith('- Suggestion:') or line.startswith('Suggestion:'):
                current_suggestion['suggestion'] = line.split(':', 1)[1].strip()
            elif line.startswith('- Line Number:') or line.startswith('Line Number:'):
                current_suggestion['line_number'] = line.split(':', 1)[1].strip()
        
        # Add the last suggestion
        if current_suggestion and 'type' in current_suggestion:
            suggestion = self._create_suggestion_from_dict(current_suggestion, file_content, repository, branch)
            if suggestion:
                suggestions.append(suggestion)
        
        return suggestions
    
    def _create_suggestion_from_dict(self, suggestion_dict: Dict[str, str], 
                                   file_content: GitHubFileContent,
                                   repository: str, branch: str) -> Optional[CodeReviewSuggestion]:
        """Create a CodeReviewSuggestion from parsed dictionary"""
        try:
            # Parse line number
            line_number = None
            if 'line_number' in suggestion_dict:
                try:
                    line_number = int(suggestion_dict['line_number'])
                except ValueError:
                    pass
            
            # Generate GitHub URL
            github_url = self._generate_github_url(repository, branch, file_content.filename, line_number)
            
            # Create suggestion
            suggestion = CodeReviewSuggestion(
                file_path=file_content.filename,
                line_number=line_number,
                suggestion_type=SuggestionType(suggestion_dict.get('type', 'improvement')),
                severity=Severity(suggestion_dict.get('severity', 'medium')),
                title=suggestion_dict.get('title', 'Code Review Suggestion'),
                description=suggestion_dict.get('description', ''),
                suggestion=suggestion_dict.get('suggestion'),
                github_url=github_url,
                rule_applied=suggestion_dict.get('type', 'improvement'),
                context_lines=file_content.context_lines
            )
            
            return suggestion
            
        except Exception as e:
            print(f"❌ Error creating suggestion: {e}")
            return None
    
    def _generate_github_url(self, repository: str, branch: str, filename: str, 
                            line_number: Optional[int] = None) -> str:
        """Generate GitHub URL for the suggestion"""
        base_url = f"https://github.com/{repository}/blob/{branch}/{filename}"
        if line_number:
            return f"{base_url}#L{line_number}"
        return base_url
