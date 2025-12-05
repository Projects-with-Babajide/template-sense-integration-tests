"""Pydantic models for API responses."""

from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    """Schema for health check endpoint."""

    status: str = Field(..., description="Service status")
    version: str = Field(..., description="Application version")
    provider: str = Field(..., description="Configured AI provider")
    model: str = Field(..., description="Configured AI model")


class ErrorResponse(BaseModel):
    """Schema for error responses."""

    detail: str = Field(..., description="Error message")


class AnalyzeResponse(BaseModel):
    """Schema for template analysis responses."""

    success: bool = Field(..., description="Whether analysis succeeded")
    data: Optional[dict[str, Any]] = Field(
        None, description="Extracted template metadata as JSON"
    )
    error: Optional[str] = Field(None, description="Error message if failed")
