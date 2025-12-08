# Template Sense Integration Tests

[![CI](https://github.com/Projects-with-Babajide/template-sense-integration-tests/workflows/CI/badge.svg)](https://github.com/Projects-with-Babajide/template-sense-integration-tests/actions)

Integration testing environment for the Template Sense package with a FastAPI UI for
analyzing Excel templates.

## Overview

This repository contains a FastAPI application and integration tests to validate the Template Sense package in a realistic environment before deployment to production.

## Quick Start

```bash
# Clone the repository
git clone https://github.com/Projects-with-Babajide/template-sense-integration-tests.git
cd template-sense-integration-tests

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your API keys

# Run the application
uvicorn app.main:app --reload
```

## Local Development

### Prerequisites

- Python 3.10+
- OpenAI or Anthropic API key
- Template Sense package installed

### Running the Application

```bash
# Activate virtual environment
source .venv/bin/activate

# Start the FastAPI server
uvicorn app.main:app --reload --port 8000
```

The application will be available at `http://localhost:8000`.

### API Endpoints

- `GET /` - Renders a Pico CSS-powered HTML form for uploading Excel files (.xlsx or .xls).
- `GET /health` - Health check returning status, configured AI provider, and model.
- `POST /analyze` - Accepts a multipart file upload, validates extension/size (max 10 MB),
  and returns extracted template metadata as JSON.

### Environment Variables

The FastAPI app reads the following variables (see `.env.example`):

- `TEMPLATE_SENSE_AI_PROVIDER` - AI provider to use (default: `openai`).
- `TEMPLATE_SENSE_AI_MODEL` - Provider-specific model (default: `gpt-4o-mini`).
- `TEMPLATE_SENSE_LOG_LEVEL` - Logging level (`INFO` by default).
- `PORT` - Port for local development (default `8000`).
- `OPENAI_API_KEY` or `ANTHROPIC_API_KEY` - Provider credentials required by
  `template-sense`.

### Using the Web UI

1. Start the server with `uvicorn app.main:app --reload --port 8000`.
2. Open `http://localhost:8000` in your browser.
3. Upload an Excel file (`.xlsx` or `.xls`, up to 10 MB).
4. View the extracted JSON metadata in the on-page results area. Errors are displayed in a
   friendly alert.

## Render Deployment

This application is configured for automatic deployment to Render.com using the `render.yaml` Blueprint configuration.

### Prerequisites

- A Render.com account (free tier supported)
- GitHub repository connected to Render
- AI provider API key (OpenAI or Anthropic)

### Deployment Steps

1. **Connect Repository to Render**
   - Log in to [Render.com](https://render.com)
   - Click "New +" and select "Blueprint"
   - Connect your GitHub account if not already connected
   - Select this repository: `Projects-with-Babajide/template-sense-integration-tests`
   - Render will automatically detect the `render.yaml` file

2. **Configure Environment Variables**

   In the Render dashboard, navigate to your service and set these environment variables:

   **Required:**
   - `TEMPLATE_SENSE_AI_PROVIDER` - Set to `openai` or `anthropic`
   - `OPENAI_API_KEY` - Your OpenAI API key (if using OpenAI)
   - `ANTHROPIC_API_KEY` - Your Anthropic API key (if using Anthropic)

   **Optional:**
   - `TEMPLATE_SENSE_AI_MODEL` - Specific model to use (e.g., `gpt-4o-mini`, `claude-3-5-sonnet-20241022`)
   - `TEMPLATE_SENSE_LOG_LEVEL` - Set to `DEBUG`, `INFO`, `WARNING`, or `ERROR` (default: `INFO`)

3. **Deploy from Main Branch**
   - Render will automatically deploy when you push to the `main` branch
   - Manual deploys can be triggered from the Render dashboard
   - Build time: ~2-3 minutes on free tier

4. **Access Your Live Application**
   - Once deployed, Render provides a public HTTPS URL
   - Format: `https://template-sense-integration-tests.onrender.com`
   - Health check endpoint: `https://your-app.onrender.com/health`
   - Web UI: `https://your-app.onrender.com/`

### Configuration Details

The `render.yaml` file configures:
- **Service type:** Web service
- **Runtime:** Python
- **Plan:** Free tier (suitable for testing and demos)
- **Build command:** `pip install -r requirements.txt`
- **Start command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- **Health check:** `/health` endpoint for automatic health monitoring
- **Auto-deploy:** Enabled for `main` branch

### Troubleshooting

**Build Failures:**
- Verify `requirements.txt` includes all dependencies
- Check Python version compatibility (3.10+ required)

**Deployment Issues:**
- Ensure environment variables are set correctly in Render dashboard
- Check that at least one AI provider API key is configured
- Verify the health check endpoint returns 200 OK

**Free Tier Limitations:**
- Service may spin down after 15 minutes of inactivity
- First request after spin-down may take 30-60 seconds to respond
- Consider upgrading to a paid plan for production use

## Running Tests

### Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Configure environment variables:
   ```bash
   cp .env.example .env
   # Edit .env and add your API keys
   ```

3. Set AI provider API key:
   ```bash
   # For OpenAI
   export OPENAI_API_KEY=sk-...

   # OR for Anthropic
   export ANTHROPIC_API_KEY=sk-ant-...
   ```

### Run Tests

```bash
# Run all tests
pytest

# Run only unit tests (no AI calls)
pytest -m "not integration"

# Run integration tests (with real AI provider)
pytest -m integration

# Run with coverage report
pytest --cov=tests --cov-report=html

# Run specific test file
pytest tests/test_basic_import.py -v
```

#### Troubleshooting

- If you see `ModuleNotFoundError: No module named "fastapi"` during test collection, ensure you ran `pip install -r requirements.txt` inside your virtual environment before invoking `pytest`.

### Test Structure

- `tests/test_basic_import.py` - Package import validation
- `tests/test_analyzer_integration.py` - End-to-end integration tests
- `tests/fixtures/` - Sample Excel files for testing

## Continuous Integration

This project uses GitHub Actions for automated testing and code quality checks on every push and pull request.

### Workflow Overview

Every push and pull request to the `main` branch triggers three jobs:

1. **Code Quality** - Black formatting and Ruff linting checks (Python 3.12)
2. **Unit Tests** - Fast tests without AI provider calls, run across Python 3.10, 3.11, 3.12, and 3.13
3. **Integration Tests** - Full Template Sense integration with OpenAI (Python 3.12 only)

The workflow uses pip caching to speed up dependency installation and runs tests in parallel where possible.

### Status Badge

The badge at the top of this README shows the current CI status:
- **Passing** - All checks passed successfully
- **Failing** - One or more checks failed
- **In Progress** - Workflow currently running

Click the badge to view detailed workflow runs and logs in the [Actions tab](https://github.com/Projects-with-Babajide/template-sense-integration-tests/actions).

### Required GitHub Secrets

For integration tests to pass in CI, the following GitHub Secret must be configured:

- `OPENAI_API_KEY` - OpenAI API key for Template Sense integration tests

**To add secrets:**
1. Go to repository Settings → Secrets and variables → Actions
2. Click "New repository secret"
3. Add `OPENAI_API_KEY` with your API key value

See [GitHub Secrets documentation](https://docs.github.com/en/actions/security-guides/encrypted-secrets) for detailed setup instructions.

### Workflow Details

**Jobs:**
- **lint**: Runs Black (formatting check) and Ruff (linting) on Python 3.12
- **test**: Runs unit tests on Python 3.10, 3.11, 3.12, and 3.13 in parallel
- **integration-test**: Runs integration tests with real AI provider on Python 3.12 (only after unit tests pass)

**Artifacts:**
- Coverage reports are uploaded as artifacts for each test run
- Artifacts are retained for 30 days and can be downloaded from workflow run pages

## Environment Variables

See `.env.example` for required environment variables:

- `TEMPLATE_SENSE_AI_PROVIDER` - AI provider to use ("openai" or "anthropic")
- `OPENAI_API_KEY` - OpenAI API key (if using OpenAI)
- `ANTHROPIC_API_KEY` - Anthropic API key (if using Anthropic)

## Project Structure

```
template-sense-integration-tests/
├── app/                    # FastAPI application
├── tests/                  # Integration tests
│   └── fixtures/          # Sample Excel files for testing
├── .env.example           # Environment variable template
├── .gitignore            # Git ignore rules
└── README.md             # This file
```

## License

This project is part of the Tako AI Enablement initiative.
