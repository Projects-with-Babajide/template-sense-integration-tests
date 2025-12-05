# Template Sense Integration Tests

Integration testing environment for the Template Sense package.

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

## Render Deployment

Instructions for deploying the application to Render.com will be added here.

## Running Tests

```bash
# Run all integration tests
pytest tests/

# Run with verbose output
pytest tests/ -v

# Run specific test file
pytest tests/test_api.py -v
```

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
