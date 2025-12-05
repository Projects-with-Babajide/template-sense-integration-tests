"""FastAPI application entry point."""

from __future__ import annotations

import os
import tempfile
from pathlib import Path

from fastapi import FastAPI, File, HTTPException, Request, UploadFile, status
from fastapi.concurrency import run_in_threadpool
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates

from app.constants import (
    ALLOWED_FILE_EXTENSIONS,
    MAX_FILE_SIZE_BYTES,
    MAX_FILE_SIZE_MB,
    DEFAULT_MODEL,
    DEFAULT_PROVIDER,
    ENV_MODEL,
    ENV_PROVIDER,
)
from app.models import AnalyzeResponse, HealthResponse
from app.services.analyzer import AnalyzerService
from template_sense.errors import AIProviderError

app = FastAPI(title="Template Sense Integration API")
templates = Jinja2Templates(directory=str(Path(__file__).parent / "templates"))

analyzer_service = AnalyzerService()


def _validate_file(upload: UploadFile) -> None:
    """Validate uploaded file extension."""

    extension = Path(upload.filename or "").suffix.lower()
    if extension not in ALLOWED_FILE_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid file type. Allowed extensions: {', '.join(ALLOWED_FILE_EXTENSIONS)}",
        )


async def _save_upload_to_temp(upload: UploadFile) -> Path:
    """Save upload to a temporary file after validating size."""

    content = await upload.read()
    if not content:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No file content received.",
        )

    if len(content) > MAX_FILE_SIZE_BYTES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File is too large. Maximum allowed size is {MAX_FILE_SIZE_MB} MB.",
        )

    suffix = Path(upload.filename or "").suffix
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
        temp_file.write(content)
        temp_path = Path(temp_file.name)

    return temp_path


@app.get("/", response_class=HTMLResponse)
async def root(request: Request) -> HTMLResponse:
    """Render the upload form UI."""

    return templates.TemplateResponse(
        request,
        "index.html",
        {"request": request},
    )


@app.get("/health", response_model=HealthResponse)
async def health() -> HealthResponse:
    """Return basic service health information."""

    provider = os.getenv(ENV_PROVIDER, DEFAULT_PROVIDER)
    model = os.getenv(ENV_MODEL, DEFAULT_MODEL)
    return HealthResponse(
        status="ok",
        version="1.0.0",
        provider=provider,
        model=model,
    )


@app.post("/analyze", response_model=AnalyzeResponse)
async def analyze(file: UploadFile = File(...)) -> JSONResponse:
    """Analyze an uploaded Excel file and return extracted metadata."""

    if not file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No file provided.",
        )

    _validate_file(file)

    temp_path: Path | None = None
    try:
        temp_path = await _save_upload_to_temp(file)
        result = await run_in_threadpool(analyzer_service.analyze, temp_path)
    except HTTPException:
        raise
    except AIProviderError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc
    except FileNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to analyze template. Please try again later.",
        ) from exc
    finally:
        if temp_path and temp_path.exists():
            temp_path.unlink(missing_ok=True)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=AnalyzeResponse(success=True, data=result, error=None).model_dump(),
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    """Return structured error responses."""

    error_response = AnalyzeResponse(success=False, data=None, error=exc.detail)
    return JSONResponse(
        status_code=exc.status_code,
        content=error_response.model_dump(),
    )


@app.exception_handler(Exception)
async def unhandled_exception_handler(
    request: Request, exc: Exception  # noqa: ARG001
) -> JSONResponse:
    """Handle unexpected errors with a generic message."""

    error_response = AnalyzeResponse(
        success=False,
        data=None,
        error="An unexpected error occurred. Please try again later.",
    )
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=error_response.model_dump(),
    )
