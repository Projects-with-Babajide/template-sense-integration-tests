"""Project-wide constants for configuration and validation."""

from __future__ import annotations

from pathlib import Path

ALLOWED_FILE_EXTENSIONS: set[str] = {".xlsx", ".xls"}
MAX_FILE_SIZE_MB: int = 10
MAX_FILE_SIZE_BYTES: int = MAX_FILE_SIZE_MB * 1024 * 1024

ENV_PROVIDER: str = "TEMPLATE_SENSE_AI_PROVIDER"
ENV_MODEL: str = "TEMPLATE_SENSE_AI_MODEL"
ENV_LOG_LEVEL: str = "TEMPLATE_SENSE_LOG_LEVEL"
ENV_PORT: str = "PORT"

DEFAULT_PROVIDER: str = "openai"
DEFAULT_MODEL: str = "gpt-4o-mini"
DEFAULT_LOG_LEVEL: str = "INFO"

DEFAULT_FIELD_DICTIONARY: dict[str, dict[str, str]] = {
    "headers": {
        "invoice_number": "Invoice number",
        "invoice_date": "Invoice date",
        "shipper_name": "Shipper",
        "consignee_name": "Consignee",
        "total_amount": "Total amount",
    },
    "columns": {
        "item": "Item",
        "quantity": "Quantity",
        "price": "Price",
    },
}

BASE_DIR: Path = Path(__file__).resolve().parent
