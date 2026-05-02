from fastapi import FastAPI

from app.routers.health import router as health_router
from app.routers.ollama import router as ollama_router

app = FastAPI()

app.include_router(health_router)
app.include_router(ollama_router)
