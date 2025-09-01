#!/usr/bin/env python3
"""
Database migration script to create code_reviews table
for storing AI code review suggestions.
"""

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv('config.env')

# Database connection
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL not found in environment variables")

# Create engine
engine = create_engine(DATABASE_URL)

def create_code_reviews_table():
    """Create code_reviews table"""
    print("Creating code_reviews table...")
    
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS code_reviews (
        id SERIAL PRIMARY KEY,
        pull_request_id INTEGER NOT NULL,
        file_path VARCHAR(500) NOT NULL,
        line_number INTEGER,
        suggestion_type VARCHAR(50) NOT NULL,
        severity VARCHAR(20) DEFAULT 'medium',
        title VARCHAR(255) NOT NULL,
        description TEXT NOT NULL,
        suggestion TEXT,
        github_url VARCHAR(500),
        rule_applied VARCHAR(100),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        
        FOREIGN KEY (pull_request_id) REFERENCES pull_requests(id) ON DELETE CASCADE
    );
    """
    
    # Create indexes for better performance
    create_indexes_sql = [
        "CREATE INDEX IF NOT EXISTS idx_code_reviews_pr_id ON code_reviews(pull_request_id);",
        "CREATE INDEX IF NOT EXISTS idx_code_reviews_file_path ON code_reviews(file_path);",
        "CREATE INDEX IF NOT EXISTS idx_code_reviews_severity ON code_reviews(severity);"
    ]
    
    with engine.connect() as conn:
        # Create table
        conn.execute(text(create_table_sql))
        
        # Create indexes
        for index_sql in create_indexes_sql:
            conn.execute(text(index_sql))
        
        conn.commit()
        print("  ✓ code_reviews table created successfully!")
        print("  ✓ Indexes created for performance!")

def main():
    """Run the migration"""
    print("Starting code_reviews table migration...")
    print(f"Database: {DATABASE_URL.split('@')[1] if '@' in DATABASE_URL else DATABASE_URL}")
    
    try:
        # Test connection
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            print("✓ Database connection successful")
        
        # Create table
        create_code_reviews_table()
        
        print("\n🎉 Code reviews table migration completed successfully!")
        print("\nTable structure:")
        print("- id: Primary key")
        print("- pull_request_id: Foreign key to pull_requests")
        print("- file_path: Path to the file being reviewed")
        print("- line_number: Specific line number (if applicable)")
        print("- suggestion_type: Type of suggestion (improvement, bug, style, etc.)")
        print("- severity: low, medium, high")
        print("- title: Short title for the suggestion")
        print("- description: Detailed description of the issue")
        print("- suggestion: Specific suggestion for improvement")
        print("- github_url: Direct link to the specific line in GitHub")
        print("- rule_applied: Which custom rule was triggered")
        print("- created_at: Timestamp of when review was generated")
        
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        raise

if __name__ == "__main__":
    main()
