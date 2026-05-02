import os

from dotenv import load_dotenv


load_dotenv()

OLLAMA_BASE_URL = os.getenv('OLLAMA_BASE_URL', 'http://ollama:11434')
OLLAMA_MODEL = os.getenv('OLLAMA_MODEL', 'gemma3:270m')

DATABASE_URL = os.getenv(
    'DATABASE_URL',
    'postgresql+asyncpg://postgres:postgres@localhost:5432/postgres',
)

ALEMBIC_DATABASE_URL = os.getenv(
    'ALEMBIC_DATABASE_URL',
    'postgresql://postgres:postgres@localhost:5432/postgres',
)

LLM_TIMEOUT_SECONDS = float(os.getenv('LLM_TIMEOUT_SECONDS', '60'))
