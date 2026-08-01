import secrets

from fastapi import Depends, HTTPException, status
from fastapi.security import APIKeyHeader

from app.config import settings

api_key_header = APIKeyHeader(name = "X-API-Key", auto_error = False)

def require_api_key(provided: str | None = Depends(api_key_header)) -> None:
    """Guard write endpoints. Reads stay public."""
    if not settings.admin_api_key:
        raise HTTPException(
            status_code = status.HTTP_503_SERVICE_UNAVAILABLE,
            detail = "Write access is not configured on this instance.",
        )
    if not provided or not secrets.compare_digest(provided, settings.admin_api_key):
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Invalid or missing API key.",
        )