from fastapi import APIRouter

from app.schemas import GenerateRequest, GenerateResponse
from app.services.ollama import generate_text, get_models

router = APIRouter(tags=["ollama"])


@router.get("/")
def read_root() -> dict[str, str]:
    return {"message": "Hello from ollama-text-gateway"}


@router.get("/models")
async def models() -> dict[str, list[dict[str, str]]]:
    return await get_models()


@router.post("/generate", response_model=GenerateResponse)
async def generate(request: GenerateRequest) -> GenerateResponse:
    return await generate_text(request.prompt)
