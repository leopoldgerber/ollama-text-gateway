import httpx
from fastapi import HTTPException

from app.config import OLLAMA_BASE_URL, OLLAMA_MODEL
from app.schemas import GenerateResponse


async def _fetch_tags() -> dict:
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(f"{OLLAMA_BASE_URL}/api/tags")
            response.raise_for_status()
    except httpx.HTTPError as exc:
        raise HTTPException(
            status_code=502,
            detail=f"Ollama tags request failed: {exc}",
        ) from exc

    return response.json()


async def get_models() -> dict[str, list[dict[str, str]]]:
    data = await _fetch_tags()
    models = data.get("models", [])

    return {
        "models": [
            {
                "name": model.get("name", ""),
                "model": model.get("model", ""),
            }
            for model in models
        ]
    }


async def check_ollama_health() -> dict[str, str]:
    await _fetch_tags()
    return {"status": "ok", "ollama": "reachable"}


async def generate_text(prompt: str) -> GenerateResponse:
    if not prompt.strip():
        raise HTTPException(status_code=400, detail="Prompt must not be empty")

    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False,
    }

    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                f"{OLLAMA_BASE_URL}/api/generate",
                json=payload,
            )
            response.raise_for_status()
    except httpx.HTTPError as exc:
        raise HTTPException(
            status_code=502,
            detail=f"Ollama request failed: {exc}",
        ) from exc

    data = response.json()
    return GenerateResponse(
        response=data.get("response", ""),
        model=data.get("model", OLLAMA_MODEL),
    )
