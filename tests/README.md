# Testing Documentation

This directory contains all testing-related files organized by type and purpose.

## 📁 Directory Structure

```
tests/
├── README.md                    # This file
├── unit/                        # Unit tests and test scripts
│   ├── test_bad_code.py        # Test bad code examples
│   ├── test_webhook_local.py   # Local webhook testing
│   ├── test_connection.py      # Database connection testing
│   └── test_webhook.py         # Webhook testing scripts
├── integration/                 # Integration tests and database scripts
│   ├── init_db.py              # Database initialization
│   ├── migrate_db.py           # Basic database migration
│   ├── migrate_enhanced_schema.py # Enhanced schema migration
│   └── migrate_code_reviews_table.py # Code reviews table migration
├── fixtures/                    # Test data and sample files
│   ├── dummy_code_with_security_issues.py    # Security violation examples
│   └── dummy_code_with_subtle_issues.py      # Subtle code quality issues
└── docs/                        # Troubleshooting and debugging docs
    ├── WEBHOOK_TIMEOUT_FIX.md  # Webhook timeout resolution
    ├── WEBHOOK_HEADER_TROUBLESHOOTING.md # Header troubleshooting
    └── WEBHOOK_TROUBLESHOOTING.md # General webhook troubleshooting
```

## 🧪 Testing Categories

### **Unit Tests** (`unit/`)
- **Purpose**: Test individual components in isolation
- **Files**: Test scripts for specific functionality
- **Usage**: Run during development to verify component behavior

### **Integration Tests** (`integration/`)
- **Purpose**: Test database operations and migrations
- **Files**: Database setup, migration, and initialization scripts
- **Usage**: Run to set up test databases and verify data flow

### **Test Fixtures** (`fixtures/`)
- **Purpose**: Provide test data and sample files
- **Files**: Python files with intentional code violations
- **Usage**: Test AI agent's ability to detect rule violations

### **Documentation** (`docs/`)
- **Purpose**: Troubleshooting guides and debugging information
- **Files**: Markdown files documenting common issues and solutions
- **Usage**: Reference when encountering problems during testing

## 🚀 Running Tests

### **Unit Tests**
```bash
cd tests/unit
python test_webhook.py          # Test webhook functionality
python test_bad_code.py         # Test bad code detection
python test_connection.py       # Test database connection
```

### **Integration Tests**
```bash
cd tests/integration
python init_db.py               # Initialize test database
python migrate_db.py            # Run basic migrations
python migrate_enhanced_schema.py # Run enhanced schema
```

### **Test Fixtures**
```bash
cd tests/fixtures
# These files are used by the AI agent for testing
# They contain intentional code violations to verify rule detection
```

## 🔧 Test Configuration

### **Environment Setup**
- Copy `Api/config.env.template` to `Api/config.env`
- Configure test database credentials
- Set up test API keys and tokens

### **Database Testing**
- Use separate test database for testing
- Run migrations before running tests
- Clean up test data after testing

## 📝 Adding New Tests

### **Unit Tests**
1. Create test file in `tests/unit/`
2. Follow naming convention: `test_*.py`
3. Include proper assertions and error handling

### **Test Fixtures**
1. Create sample files in `tests/fixtures/`
2. Include intentional violations for testing
3. Document what rules are being tested

### **Integration Tests**
1. Create migration or setup scripts in `tests/integration/`
2. Test database operations and data flow
3. Include cleanup procedures

## 🐛 Troubleshooting

### **Common Issues**
- Database connection failures
- Webhook timeout errors
- API authentication problems
- File path resolution issues

### **Debugging Steps**
1. Check environment configuration
2. Verify database connectivity
3. Test individual components
4. Review troubleshooting docs in `tests/docs/`

## 📚 Related Documentation

- **Main README**: [../README.md](../README.md)
- **API Documentation**: [../Api/README.md](../Api/README.md)
- **AI Agent Docs**: [../Api/ai_agent/README.md](../Api/ai_agent/README.md)
- **Custom Rules**: [../Custom-rules/python-code-standards.md](../Custom-rules/python-code-standards.md)
