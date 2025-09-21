from fastapi import HTTPException, Header, status
from core.config import settings


async def get_api_key(x_api_key: str = Header(..., alias="X-API-Key")):
    """Verify API key from request headers"""
    if x_api_key != settings.api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return x_api_key
