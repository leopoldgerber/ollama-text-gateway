from fastapi import FastAPI
import uvicorn

from app.ollama_client import generate_text
from app.prompt_builder import build_prompt
from app.schemas import GenerateRequest, GenerateResponse


app = FastAPI(title='Project 1')


@app.post('/generate', response_model=GenerateResponse)
def create_reply(request_data: GenerateRequest) -> GenerateResponse:
    """Generate model response.
    Args:
        request_data (GenerateRequest): Request body data."""
    prompt_text = build_prompt(user_text=request_data.text)
    answer_text = generate_text(prompt_text=prompt_text)
    response_data = GenerateResponse(answer=answer_text)
    return response_data


def run_server() -> None:
    """Run HTTP server.
    Args:
        None: No arguments."""
    uvicorn.run('app.main:app', host='0.0.0.0', port=8000, reload=True)


if __name__ == '__main__':
    run_server()
