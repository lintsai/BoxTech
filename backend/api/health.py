"""
Health check API routes under /api/v1
"""

from fastapi import APIRouter

router = APIRouter(prefix="/api/v1", tags=["health"])


@router.get("/health")
async def api_health():
    return {"status": "healthy"}
