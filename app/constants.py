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

APP_VERSION: str = "1.0.0"
APP_TITLE: str = "Template Sense Integration API"

ERROR_NO_FILE_CONTENT: str = "No file content received."
ERROR_FILE_TOO_LARGE: str = "File is too large. Maximum allowed size is {max_size} MB."
ERROR_NO_FILE_PROVIDED: str = "No file provided."
ERROR_INVALID_FILE_TYPE: str = "Invalid file type. Allowed extensions: {extensions}"
ERROR_ANALYSIS_FAILED: str = "Failed to analyze template. Please try again later."
ERROR_UNEXPECTED: str = "An unexpected error occurred. Please try again later."

DEFAULT_FIELD_DICTIONARY: dict[str, dict[str, str]] = {
    "headers": {
        "due_date": "Due date",
        "invoice_number": "Invoice number",
        "invoice_date": "Invoice date",
        "notes": "Notes",
        "shipper": "Shipper",
        "consignee": "Consignee",
        "shipper_address": "Shipper address",
        "consignee_address": "Consignee address",
        "etd": "ETD",
        "eta": "ETA",
        "port_of_loading": "Port of loading",
        "port_of_discharge": "Port of discharge",
        "flight_number": "Flight number",
        "awb_number": "AWB number",
        "total_gross_weight": "Total gross weight",
        "total_boxes": "Total boxes",
        "fixed_freight_cost": "Fixed freight cost",
        "variable_freight_cost": "Variable freight cost",
        "mark": "Mark",
        "terms_of_delivery": "Terms of delivery",
        "terms_of_payment": "Terms of payment",
    },
    "columns": {
        "box_name": "Box name",
        "number_of_boxes": "Number of boxes",
        "condition": "Condition",
        "product_name": "Product name",
        "description": "Description",
        "origin": "Origin",
        "quantity": "Quantity",
        "quantity_unit": "Quantity unit",
        "net_weight": "Net weight",
        "gross_weight": "Gross weight",
        "currency": "Currency",
        "price": "Price",
        "price_unit": "Price unit",
        "cost": "Cost",
        "cost_unit": "Cost unit",
        "price_per_kg": "Price/kg",
        "amount": "Amount",
        "freight_cost": "Freight cost",
        "total_amount": "Total amount",
    },
}

BASE_DIR: Path = Path(__file__).resolve().parent
