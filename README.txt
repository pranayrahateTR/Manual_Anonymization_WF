================================================================================
  ANONYMIZATION TEST AUTOMATION FRAMEWORK
================================================================================

A comprehensive test automation framework for the Anonymization/Redaction
Workflow application using Pytest and Playwright.

================================================================================
  QUICK START
================================================================================

1. Clone the repository
2. Copy .env.example to .env and add your credentials
3. Install dependencies: pip install -r requirements.txt
4. Install browsers: playwright install
5. Run tests: pytest

📖 For detailed setup instructions, see: SETUP_GUIDE.txt

================================================================================
  FEATURES
================================================================================

✓ Page Object Model (POM) design pattern
✓ Pytest framework with fixtures and parameterization
✓ Playwright for cross-browser testing
✓ Secure credential management via environment variables
✓ Video recording of test executions
✓ Screenshot capture on failures
✓ Allure reporting integration
✓ Data-driven testing support
✓ Session-scoped fixtures for performance
✓ API scripts for role management

================================================================================
  TEST COVERAGE
================================================================================

1. Authentication Tests
   - Login validation
   - Session management

2. Approver Role Tests
   - Document search
   - Request creation workflow
   - Approval process

3. Redactor Role Tests
   - Role switching
   - Redaction operations
   - Document processing

4. End-to-End Integration Tests
   - Complete workflow from request to completion
   - Multi-role scenarios

================================================================================
  TECHNOLOGY STACK
================================================================================

- Python 3.8+
- Pytest (Testing Framework)
- Playwright (Browser Automation)
- Allure (Test Reporting)
- python-dotenv (Environment Management)
- openpyxl (Excel Data Han3dling)

================================================================================
  PROJECT STRUCTURE
================================================================================

Anonymization/
├── testcases/          # Test files and fixtures
├── pages/              # Page Object Model classes
├── utilities/          # Helper functions and utilities
├── Anonymization_api/  # API scripts for role management
├── ConfigurationData/  # Application configuration
├── .env.example        # Environment variable template
├── pytest.ini          # Pytest configuration
└── requirements.txt    # Python dependencies

================================================================================
  SECURITY
================================================================================

⚠️  IMPORTANT: This project uses environment variables for credential management.

- NEVER commit your .env file
- ALWAYS use .env.example as a template
- Credentials are loaded via python-dotenv
- .gitignore is configured to protect sensitive files

================================================================================
  RUNNING TESTS
================================================================================

Run all tests:
    pytest

Run specific test file:
    pytest testcases/test_loginTest.py

Run with video recording:
    pytest --video=on

Generate Allure report:
    pytest --alluredir=allure-results
    allure serve allure-results

Run in headless mode:
    Set HEADLESS=true in .env file

================================================================================
  REQUIREMENTS
================================================================================

- Python 3.8 or higher
- Valid credentials for Anonymization application
- Network access to the application under test
- ~300MB disk space for Playwright browsers

See requirements.txt for complete Python package dependencies.

================================================================================
  DOCUMENTATION
================================================================================

📖 SETUP_GUIDE.txt      - Complete setup and installation instructions
📖 .env.example         - Environment variable configuration template
📖 pytest.ini           - Pytest configuration and markers

================================================================================
  SUPPORT
================================================================================

For detailed setup instructions, troubleshooting, and usage examples:
See SETUP_GUIDE.txt

================================================================================
  LICENSE
================================================================================

Internal use only - Proprietary

================================================================================

Created: April 2026
Last Updated: May 2026

================================================================================
