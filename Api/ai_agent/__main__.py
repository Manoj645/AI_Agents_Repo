"""
Main entry point for the AI Code Review Agent
"""

import sys
import os
from typing import Optional

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from .review_generator import ReviewGenerator
from .config import AIConfig

def main():
    """Main function for running the AI agent directly"""
    print("🤖 AI Code Review Agent")
    print("=" * 50)
    
    # Validate configuration
    if not AIConfig.validate():
        print("❌ Configuration validation failed. Please check your environment variables.")
        sys.exit(1)
    
    # Check command line arguments
    if len(sys.argv) < 4:
        print("Usage: python -m ai_agent <owner> <repo> <pr_number>")
        print("Example: python -m ai_agent Manoj645 AI_Agents_Repo 123")
        sys.exit(1)
    
    owner = sys.argv[1]
    repo = sys.argv[2]
    pr_number = int(sys.argv[3])
    
    print(f"🔍 Starting review for PR #{pr_number} in {owner}/{repo}")
    
    # Initialize and run review
    try:
        review_generator = ReviewGenerator()
        review_result = review_generator.generate_review(owner, repo, pr_number)
        
        if review_result:
            print("\n🎉 Review completed successfully!")
            print(f"📊 Summary: {review_result.review_summary}")
            print(f"📝 Total suggestions: {review_result.total_suggestions}")
            print(f"📁 Files reviewed: {review_result.files_reviewed}")
            
            if review_result.suggestions:
                print("\n🔍 Suggestions:")
                for i, suggestion in enumerate(review_result.suggestions, 1):
                    print(f"\n{i}. {suggestion.title}")
                    print(f"   File: {suggestion.file_path}")
                    if suggestion.line_number:
                        print(f"   Line: {suggestion.line_number}")
                    print(f"   Type: {suggestion.suggestion_type.value}")
                    print(f"   Severity: {suggestion.severity.value}")
                    print(f"   Description: {suggestion.description}")
                    if suggestion.suggestion:
                        print(f"   Suggestion: {suggestion.suggestion}")
                    if suggestion.github_url:
                        print(f"   GitHub: {suggestion.github_url}")
        else:
            print("❌ Review generation failed")
            sys.exit(1)
            
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
