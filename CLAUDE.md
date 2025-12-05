# Template Sense Integration Tests — Claude Project Context Document

**Version:** 1.0
**Last Updated:** 2025-12-05
**Project:** Tako AI Enablement — Template Sense Integration Testing Environment

---

## 1. Overview

### Business Domain
Template Sense Integration Tests is a **FastAPI-based integration testing environment** for the Template Sense package. It validates the package behavior in a realistic deployment scenario before production use at **Tako**.

**Solution:**
1. Provides a **REST API** wrapper around Template Sense functionality
2. Runs **integration tests** against real Excel files with actual AI providers
3. Validates **end-to-end workflows** including file upload, processing, and response validation
4. Tests **error handling** and edge cases in a production-like environment
5. Prepares the application for **Render.com deployment**

### Primary User Types
1. **Tako Engineering Team** — Validates Template Sense before integration
2. **Automated Agents (Devin, Claude)** — Implement features, fix bugs, run tests
3. **CI/CD Pipeline** — Automated integration testing

### What This Project Does NOT Do
- No production data processing
- No persistent storage or database management
- No user authentication or authorization (test environment only)
- No UI/frontend components

---

## 2. Architecture & Patterns

### Folder Structure

```
template-sense-integration-tests/
├── app/                         # FastAPI application
│   ├── main.py                 # FastAPI app entry point
│   ├── routers/                # API route handlers
│   ├── models/                 # Pydantic request/response models
│   └── services/               # Business logic layer
├── tests/                      # Integration tests
│   ├── fixtures/               # Sample Excel files
│   ├── test_api.py            # API endpoint tests
│   └── test_integration.py    # End-to-end integration tests
├── .env.example               # Environment variable template
├── .gitignore                 # Git ignore rules
└── README.md                  # Documentation
```

### Module Boundaries and Layer Dependencies

**Dependency Flow (bottom-up):**
1. **Template Sense Package** → Core functionality (external dependency)
2. **Services** → Business logic wrapping Template Sense
3. **Models** → Pydantic schemas for request/response validation
4. **Routers** → API endpoints
5. **Main** → FastAPI application setup

**Key Principles:**
- Each layer only imports from layers below it
- No circular dependencies
- Clear separation between API layer and business logic

---

## 3. Stack Best Practices

### Language-Specific Idioms

**Python Version:** 3.10+

**Type Hints:** Required for all functions
```python
def analyze_template(file_path: str, field_dict: dict[str, list[str]]) -> dict[str, Any]:
    ...
```

**Pydantic Models:** Use for all API request/response schemas
```python
from pydantic import BaseModel, Field

class AnalyzeRequest(BaseModel):
    file_path: str = Field(..., description="Path to Excel template")
    field_dictionary: dict[str, list[str]] = Field(..., description="Canonical field dictionary")
```

**Async/Await:** Use for FastAPI endpoints
```python
@router.post("/analyze")
async def analyze_template(request: AnalyzeRequest) -> AnalyzeResponse:
    ...
```

### Constants Management

**Central Constants File:** `app/constants.py`

All configuration values must be defined and imported from this module:
```python
from app.constants import (
    MAX_FILE_SIZE_MB,
    ALLOWED_FILE_EXTENSIONS,
    API_TIMEOUT_SECONDS,
)
```

**What belongs in constants.py:**
- API configuration (timeouts, rate limits)
- File upload limits and allowed extensions
- Environment variable names
- Default values for Template Sense parameters

**Never hard-code these values** in other modules. Always import from `constants.py`.

### Framework-Specific Patterns

**FastAPI:** Use dependency injection, async handlers, Pydantic models
**Pytest:** `tests/test_<module_name>.py`, use `pytest-asyncio` for async tests
**Template Sense:** Import as external package, handle all exceptions gracefully

---

## 4. Anti-Patterns

### ❌ NEVER Do This:
1. **Log sensitive data** — No API keys, file contents, full file paths
2. **Hard-code secrets** — Use environment variables only
3. **Use print()** — Use FastAPI logging or Python logging module
4. **Return raw exceptions to API clients** — Always catch and return structured error responses
5. **Store uploaded files permanently** — Clean up temporary files after processing
6. **Hard-code configuration values** — Use constants from `app/constants.py`
7. **Skip input validation** — Always validate file types, sizes, and request payloads

### ✅ ALWAYS Do This:
1. **Validate inputs early** at API boundary with Pydantic models
2. **Use async/await** for all FastAPI endpoints
3. **Handle Template Sense exceptions** gracefully with proper error responses
4. **Clean up temporary files** after processing
5. **Import constants from `constants.py`** — All configuration values should be centralized
6. **Return consistent error responses** with proper HTTP status codes
7. **Log important events** with appropriate log levels

---

## 5. Data Models

### Core Domain Entities

**API Flow:**
```
HTTP Request → Pydantic Model → Service Layer → Template Sense →
Service Layer → Pydantic Response → HTTP Response
```

**Key Pydantic Models:**
- `AnalyzeRequest` — API request for template analysis
- `AnalyzeResponse` — API response with Template Sense output
- `ErrorResponse` — Standardized error response
- `HealthCheckResponse` — Health check endpoint response

**Example Request/Response:**
```python
# Request
{
    "file_path": "/path/to/template.xlsx",
    "field_dictionary": {
        "invoice_number": ["invoice no", "inv no"],
        "shipper_name": ["shipper", "sender"]
    }
}

# Response
{
    "status": "success",
    "template": {
        "header_fields": [...],
        "table_regions": [...]
    }
}
```

**Validation Rules:**
- File must exist and be readable
- File must be `.xlsx` or `.xls` format
- File size must not exceed configured limit
- Field dictionary must be valid JSON object

---

## 6. Configuration, Security, and Authentication

### Environment Variable Management

**Required:**
```bash
TEMPLATE_SENSE_AI_PROVIDER=openai  # or "anthropic"
OPENAI_API_KEY=sk-...              # if using OpenAI
ANTHROPIC_API_KEY=sk-...           # if using Anthropic
```

**Optional:**
```bash
TEMPLATE_SENSE_AI_MODEL=gpt-4      # Provider-specific model
TEMPLATE_SENSE_LOG_LEVEL=INFO      # DEBUG, INFO, WARNING, ERROR
PORT=8000                          # FastAPI server port
```

### Secrets Handling
- Never log API keys (even partially)
- Never commit `.env` files
- Use `python-dotenv` for local dev
- Use Render environment variables for deployment

### API Security Patterns
- Validate file paths (no directory traversal)
- Generic errors to external callers
- Rate limiting (if needed)
- File size limits to prevent DoS

---

## 7. Testing Strategy

### Integration Tests
- Located in `tests/test_*.py`
- Tests against real Template Sense package
- Uses actual AI providers (with test API keys)
- Coverage target: 80%+
- Run: `pytest tests/`

### Test Fixtures
- Sample Excel files in `tests/fixtures/`
- Test field dictionaries
- Mock responses for edge cases

### Testing Checklist
- API endpoint functionality
- Error handling (invalid files, missing fields)
- File upload and cleanup
- Template Sense integration
- Response format validation

---

## 8. Development Workflow

### Setting Up the Environment
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your API keys
uvicorn app.main:app --reload
```

### Code Quality Tools
- **Black:** `black .`
- **Ruff:** `ruff check .`
- **Pytest:** `pytest tests/`

### Git Workflow
- Main branch: `main`
- Feature branches: **MUST use the branch name from Linear ticket**
- Commit messages: Follow conventional commits format

---

## 9. How Claude Should Use This Document

### When Implementing a New Feature
1. Review **Architecture & Patterns**
2. Check **Data Models** for required schemas
3. Follow **Stack Best Practices**
4. Avoid **Anti-Patterns**
5. Add integration tests

### When Fixing a Bug
1. Identify which layer the bug is in (API, Service, or Template Sense)
2. Check **Data Models** to understand expected flow
3. Add a regression test

---

## 10. Future Enhancements

**Planned:**
- Render.com deployment configuration
- CI/CD pipeline integration
- Performance testing
- Load testing endpoints

**Not Planned:**
- Production data processing
- User authentication/authorization
- Database integration
- Frontend UI

---

## 11. Contact and Support

**Primary Maintainer:** Babajide (Tako AI Enablement Team)
**Repository:** https://github.com/Projects-with-Babajide/template-sense-integration-tests
**Linear Workspace:** Projects with Babajide
**Linear Team:** Agentic Team
**Linear Project:** Tako AI Enablement

**Linear Integration Details:**
- **Team Name:** `Agentic Team` (use this exact name when filtering issues by team)
- **Project Name:** `Tako AI Enablement` (use this exact name when filtering issues by project)
- **Issue Pattern:** `BAT-{number}` (e.g., BAT-65, BAT-66)

**Related Repositories:**
- Template Sense Package: https://github.com/Projects-with-Babajide/template-sense

---

**End of Document**
