#!/usr/bin/env python3
"""
Database migration script to add custom_rules table
"""

import os
import sys
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from models import CustomRule, RuleCategory, ProgrammingLanguage
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv("config.env")

# Database URL
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:password@localhost:5432/pr_review_db")

def create_custom_rules_table():
    """Create the custom_rules table if it doesn't exist"""
    
    # Get database URL
    engine = create_engine(DATABASE_URL)
    
    try:
        # Check if custom_rules table exists
        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_schema = 'public' 
                    AND table_name = 'custom_rules'
                );
            """))
            table_exists = result.scalar()
            
            if table_exists:
                print("✅ Custom rules table already exists")
                return True
            
            print("📝 Creating custom_rules table...")
            
            # Create the custom_rules table
            conn.execute(text("""
                CREATE TABLE custom_rules (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    filename VARCHAR(255) NOT NULL,
                    content TEXT NOT NULL,
                    language VARCHAR(50) NOT NULL,
                    category VARCHAR(50) NOT NULL DEFAULT 'General',
                    description TEXT,
                    is_active BOOLEAN NOT NULL DEFAULT TRUE,
                    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
                    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
                );
            """))
            
            # Create indexes for better performance
            conn.execute(text("""
                CREATE INDEX idx_custom_rules_language ON custom_rules(language);
                CREATE INDEX idx_custom_rules_category ON custom_rules(category);
                CREATE INDEX idx_custom_rules_is_active ON custom_rules(is_active);
                CREATE INDEX idx_custom_rules_created_at ON custom_rules(created_at);
            """))
            
            conn.commit()
            print("✅ Custom rules table created successfully")
            
            # Insert sample data
            insert_sample_data(engine)
            
            return True
        else:
            # Table exists, just insert sample data
            insert_sample_data(engine)
            return True
            
    except Exception as e:
        print(f"❌ Error creating custom rules table: {e}")
        return False

def insert_sample_data(engine):
    """Insert sample custom rules data"""
    
    try:
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        db = SessionLocal()
        
        # Check if sample data already exists
        existing_rules = db.query(CustomRule).count()
        if existing_rules > 0:
            print(f"ℹ️  Found {existing_rules} existing rules, adding more sample data...")
        
        print("📝 Inserting sample custom rules...")
        
        # Sample Python code standards rule
        python_rule = CustomRule(
            name="Python Code Standards",
            filename="python-code-standards.md",
            content="""# Python Code Standards for AI Code Review

## 🎯 **Code Quality Rules**

### **1. Function Length & Complexity**
- **Rule**: Functions should not exceed 15 lines of code
- **Reason**: Improves readability, testability, and maintainability
- **Example**: Break large functions into smaller, focused functions

### **2. Variable Naming Conventions**
- **Rule**: Use descriptive, snake_case names for variables and functions
- **Reason**: Enhances code readability and understanding
- **Examples**:
  - ✅ `user_count`, `calculate_total_price()`
  - ❌ `cnt`, `calc()`, `temp`

### **3. Import Organization**
- **Rule**: Group imports: standard library, third-party, local modules
- **Reason**: Clear dependency structure and easier maintenance""",
            language=ProgrammingLanguage.PYTHON,
            category=RuleCategory.STYLE,
            description="Comprehensive Python coding standards and best practices",
            is_active=True
        )
        
        # Sample JavaScript best practices rule
        js_rule = CustomRule(
            name="JavaScript Best Practices",
            filename="javascript-standards.md",
            content="""# JavaScript Best Practices

## 🎯 **Code Quality Rules**

### **1. Variable Naming**
- **Rule**: Use camelCase for variables and functions
- **Rule**: Use PascalCase for classes and constructors
- **Examples**:
  - ✅ `userCount`, `calculateTotalPrice()`, `UserProfile`
  - ❌ `user_count`, `calc()`, `userprofile`

### **2. Function Structure**
- **Rule**: Keep functions small and focused
- **Rule**: Use early returns to reduce nesting
- **Example**:
  ```javascript
  function processUser(user) {
      if (!user) return null;
      if (!user.isActive) return null;
      return processActiveUser(user);
  }
  ```

### **3. Error Handling**
- **Rule**: Always handle promises with try-catch or .catch()
- **Rule**: Use specific error types when possible""",
            language=ProgrammingLanguage.JAVASCRIPT,
            category=RuleCategory.STYLE,
            description="JavaScript coding standards and best practices",
            is_active=True
        )
        
        # Sample security rule
        security_rule = CustomRule(
            name="Security Best Practices",
            filename="security-standards.md",
            content="""# Security Best Practices

## 🔒 **Security Rules**

### **1. Input Validation**
- **Rule**: Always validate and sanitize user input
- **Rule**: Use parameterized queries to prevent SQL injection
- **Rule**: Validate file uploads and restrict file types

### **2. Authentication & Authorization**
- **Rule**: Use secure authentication methods
- **Rule**: Implement proper session management
- **Rule**: Use HTTPS for all sensitive data transmission

### **3. Data Protection**
- **Rule**: Never store passwords in plain text
- **Rule**: Use environment variables for sensitive configuration
- **Rule**: Implement proper access controls""",
            language=ProgrammingLanguage.TEXT,
            category=RuleCategory.SECURITY,
            description="Security best practices for web applications",
            is_active=True
        )
        
        # Add rules to database
        db.add(python_rule)
        db.add(js_rule)
        db.add(security_rule)
        db.commit()
        
        print("✅ Sample custom rules inserted successfully")
        
    except Exception as e:
        print(f"❌ Error inserting sample data: {e}")
        db.rollback()
    finally:
        db.close()

def main():
    """Main migration function"""
    print("🚀 Starting custom rules table migration...")
    
    success = create_custom_rules_table()
    
    if success:
        print("✅ Migration completed successfully!")
        print("\n📋 Available endpoints:")
        print("  GET    /custom-rules")
        print("  GET    /custom-rules/{rule_id}")
        print("  POST   /custom-rules")
        print("  PUT    /custom-rules/{rule_id}")
        print("  DELETE /custom-rules/{rule_id}")
        print("  POST   /custom-rules/upload")
    else:
        print("❌ Migration failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()
