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
            print(f"🔍 Loading custom rules from: {rules_path}")
            print(f"🔍 Current working directory: {os.getcwd()}")
            print(f"🔍 Rules file exists: {os.path.exists(rules_path)}")
            
            if os.path.exists(rules_path):
                with open(rules_path, 'r', encoding='utf-8') as f:
                    rules_content = f.read()
                    print(f"✅ Successfully loaded custom rules ({len(rules_content)} characters)")
                    return rules_content
            else:
                print(f"⚠️ Custom rules file not found: {rules_path}")
                print(f"⚠️ Trying absolute path: {os.path.abspath(rules_path)}")
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
            
            print(f"🤖 Analyzing file: {file_content.filename}")
            print(f"📏 File size: {file_content.size} bytes")
            print(f"📝 Content length: {len(file_content.content)} characters")
            print(f"🔍 Custom rules loaded: {len(self.custom_rules)} characters")
            
            # Get AI analysis
            print(f"🚀 Sending to OpenAI for analysis...")
            response = self.llm.invoke([
                SystemMessage(content="You are an expert Python code reviewer. Analyze the code and provide specific, actionable suggestions."),
                HumanMessage(content=analysis_prompt)
            ])
            
            print(f"📥 AI Response received: {len(response.content)} characters")
            print(f"📄 AI Response preview: {response.content[:200]}...")
            
            # Parse suggestions
            suggestions = self._parse_ai_response(response.content, file_content, repository, branch)
            
            print(f"✅ Parsed {len(suggestions)} suggestions")
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
        
        ## CRITICAL: You MUST find violations!
        
        ## Analysis Instructions:
        1. CAREFULLY review the code against EVERY custom rule above
        2. Look for ANY violations, no matter how small
        3. Be STRICT and thorough - don't let anything slide
        4. Focus on the changed lines and their context
        5. Provide specific, actionable suggestions
        6. Include line numbers where applicable
        7. Categorize suggestions by type and severity
        
        ## IMPORTANT: If you find ANY violations, you MUST provide suggestions.
        ## Only respond with "CODE_QUALITY_GOOD" if the code is PERFECT.
        
        ## Response Format:
        For each suggestion, provide:
        - Type: improvement/bug/style/security/performance/documentation/testing
        - Severity: low/medium/high/critical
        - Title: Short descriptive title
        - Description: Detailed explanation of the issue
        - Suggestion: Specific recommendation for improvement
        - Line Number: The specific line(s) affected
        
        ## Example Response:
        - Type: style
        - Severity: medium
        - Title: Function too long
        - Description: Function exceeds 15 lines limit
        - Suggestion: Break into smaller functions
        - Line Number: 25-45
        
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
        
        print(f"🔍 Parsing AI response...")
        print(f"📄 Response length: {len(response)} characters")
        
        # Check if code quality is good
        if "CODE_QUALITY_GOOD" in response.upper():
            print(f"✅ AI says code quality is good")
            return []
        
        # Parse suggestions with enhanced pattern matching
        lines = response.split('\n')
        current_suggestion = {}
        
        print(f"🔍 Parsing {len(lines)} lines...")
        
        for i, line in enumerate(lines):
            line = line.strip()
            print(f"📝 Line {i+1}: {line[:100]}...")
            
            # Look for suggestion patterns (handle both markdown and plain text)
            if any(pattern in line for pattern in ['Type:', '**Type**:']):
                if current_suggestion and 'type' in current_suggestion:
                    # Save previous suggestion
                    print(f"💾 Saving suggestion: {current_suggestion}")
                    suggestion = self._create_suggestion_from_dict(current_suggestion, file_content, repository, branch)
                    if suggestion:
                        suggestions.append(suggestion)
                
                # Start new suggestion - extract type from various formats
                if '**Type**:' in line:
                    type_value = line.split('**Type**:', 1)[1].strip()
                elif 'Type:' in line:
                    type_value = line.split('Type:', 1)[1].strip()
                else:
                    type_value = line.split(':', 1)[1].strip()
                
                # Clean up the type value (remove asterisks and normalize)
                type_value = type_value.replace('*', '').strip().lower()
                current_suggestion = {'type': type_value}
                print(f"🆕 New suggestion started: {current_suggestion}")
                
            elif '**Severity**:' in line or 'Severity:' in line:
                if '**Severity**:' in line:
                    severity_value = line.split('**Severity**:', 1)[1].strip()
                elif 'Severity:' in line:
                    severity_value = line.split('Severity:', 1)[1].strip()
                # Clean up the severity value (remove asterisks and normalize)
                severity_value = severity_value.replace('*', '').strip().lower()
                current_suggestion['severity'] = severity_value
                print(f"🔴 Severity set: {current_suggestion.get('severity')}")
                    
            elif '**Title**:' in line or 'Title:' in line:
                if '**Title**:' in line:
                    title_value = line.split('**Title**:', 1)[1].strip()
                elif 'Title:' in line:
                    title_value = line.split('Title:', 1)[1].strip()
                # Clean up the title value (remove asterisks)
                title_value = title_value.replace('*', '').strip()
                current_suggestion['title'] = title_value
                print(f"📌 Title set: {current_suggestion.get('title')}")
                    
            elif '**Description**:' in line or 'Description:' in line:
                if '**Description**:' in line:
                    desc_value = line.split('**Description**:', 1)[1].strip()
                elif 'Description:' in line:
                    desc_value = line.split('Description:', 1)[1].strip()
                # Clean up the description value (remove asterisks)
                desc_value = desc_value.replace('*', '').strip()
                current_suggestion['description'] = desc_value
                print(f"📝 Description set: {current_suggestion.get('description')}")
                    
            elif '**Suggestion**:' in line or 'Suggestion:' in line:
                if '**Suggestion**:' in line:
                    sugg_value = line.split('**Suggestion**:', 1)[1].strip()
                elif 'Suggestion:' in line:
                    sugg_value = line.split('Suggestion:', 1)[1].strip()
                # Clean up the suggestion value (remove asterisks)
                sugg_value = sugg_value.replace('*', '').strip()
                current_suggestion['suggestion'] = sugg_value
                print(f"💡 Suggestion set: {current_suggestion.get('suggestion')}")
                    
            elif '**Line Number**:' in line or 'Line Number:' in line:
                if '**Line Number**:' in line:
                    current_suggestion['line_number'] = line.split('**Line Number**:', 1)[1].strip()
                elif 'Line Number:' in line:
                    current_suggestion['line_number'] = line.split('Line Number:', 1)[1].strip()
                print(f"📍 Line number set: {current_suggestion.get('line_number')}")
        
        # Add the last suggestion
        if current_suggestion and 'type' in current_suggestion:
            print(f"💾 Saving final suggestion: {current_suggestion}")
            suggestion = self._create_suggestion_from_dict(current_suggestion, file_content, repository, branch)
            if suggestion:
                suggestions.append(suggestion)
                print(f"✅ Suggestion created successfully")
            else:
                print(f"❌ Failed to create suggestion from: {current_suggestion}")
        
        print(f"🎯 Total suggestions parsed: {len(suggestions)}")
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
            
            # Validate and normalize suggestion type
            suggestion_type = suggestion_dict.get('type', 'improvement')
            try:
                suggestion_type_enum = SuggestionType(suggestion_type)
            except ValueError:
                # Map common variations to valid enum values
                type_mapping = {
                    'performance': 'performance',
                    'style': 'style',
                    'security': 'security',
                    'bug': 'bug',
                    'improvement': 'improvement',
                    'documentation': 'documentation',
                    'testing': 'testing'
                }
                suggestion_type = type_mapping.get(suggestion_type, 'improvement')
                suggestion_type_enum = SuggestionType(suggestion_type)
            
            # Validate and normalize severity
            severity = suggestion_dict.get('severity', 'medium')
            try:
                severity_enum = Severity(severity)
            except ValueError:
                # Map common variations to valid enum values
                severity_mapping = {
                    'low': 'low',
                    'medium': 'medium',
                    'high': 'high',
                    'critical': 'critical'
                }
                severity = severity_mapping.get(severity, 'medium')
                severity_enum = Severity(severity)
            
            # Create suggestion
            suggestion = CodeReviewSuggestion(
                file_path=file_content.filename,
                line_number=line_number,
                suggestion_type=suggestion_type_enum,
                severity=severity_enum,
                title=suggestion_dict.get('title', 'Code Review Suggestion'),
                description=suggestion_dict.get('description', ''),
                suggestion=suggestion_dict.get('suggestion'),
                github_url=github_url,
                rule_applied=suggestion_type,
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
