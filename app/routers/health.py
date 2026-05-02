from fastapi import APIRouter

from app.db.db import check_database
from app.services.ollama import check_ollama_health

router = APIRouter(tags=["health"])


@router.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@router.get("/health/ollama")
async def health_ollama() -> dict[str, str]:
    return await check_ollama_health()


@router.get('/health/db')
async def health_db() -> dict[str, str]:
    if await check_database():
        return {'status': 'ok', 'database': 'reachable'}

    return {'status': 'error', 'database': 'unreachable'}
