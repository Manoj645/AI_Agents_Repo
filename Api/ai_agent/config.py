"""
Configuration for the AI Code Review Agent
"""

import os
from dotenv import load_dotenv
from typing import Optional

# Load environment variables
load_dotenv('config.env')

class AIConfig:
    """AI Agent Configuration"""
    
    # OpenAI Configuration
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4o")
    
    # GitHub Configuration
    GITHUB_TOKEN: Optional[str] = os.getenv("GITHUB_TOKEN")
    GITHUB_API_BASE: str = "https://api.github.com"
    
    # AI Agent Configuration
    MAX_TOKENS: int = int(os.getenv("MAX_TOKENS", "4000"))
    TEMPERATURE: float = float(os.getenv("TEMPERATURE", "0.1"))
    
    # Code Review Configuration
    CONTEXT_LINES: int = int(os.getenv("CONTEXT_LINES", "5"))  # Lines before/after diff
    MAX_FILE_SIZE: int = int(os.getenv("MAX_FILE_SIZE", "1000000"))  # 1MB max file size
    
    # Custom Rules Path
    CUSTOM_RULES_PATH: str = os.getenv("CUSTOM_RULES_PATH", "../Custom-rules/python-code-standards.md")
    
    @classmethod
    def validate(cls) -> bool:
        """Validate required configuration"""
        required_vars = ["OPENAI_API_KEY", "GITHUB_TOKEN"]
        missing_vars = [var for var in required_vars if not getattr(cls, var)]
        
        if missing_vars:
            print(f"❌ Missing required environment variables: {', '.join(missing_vars)}")
            print("Please set these in your config.env file:")
            for var in missing_vars:
                if var == "OPENAI_API_KEY":
                    print(f"  {var}=your_openai_api_key_here")
                elif var == "GITHUB_TOKEN":
                    print(f"  {var}=your_github_token_here")
            return False
        
        print("✅ AI Agent configuration validated successfully!")
        return True
    
    @classmethod
    def get_github_headers(cls) -> dict:
        """Get GitHub API headers"""
        return {
            "Authorization": f"token {cls.GITHUB_TOKEN}",
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "PR-Review-AI-Agent/1.0"
        }
