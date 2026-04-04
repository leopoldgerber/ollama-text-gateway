from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import uvicorn


from app.exceptions import OllamaConnectionError, OllamaResponseError
from app.ollama_client import generate_text
from app.prompt_builder import build_prompt
from app.schemas import GenerateRequest, GenerateResponse


app = FastAPI(title='Ollama Text Gateway')


@app.exception_handler(OllamaConnectionError)
def handle_ollama_error(
    request: Request,
    error: OllamaConnectionError,
) -> JSONResponse:
    """Handle Ollama connection error.
    Args:
        request (Request): FastAPI request.
        error (OllamaConnectionError): Raised exception."""
    response_data = JSONResponse(
        status_code=502,
        content={'detail': str(error)},
    )
    return response_data


@app.exception_handler(OllamaResponseError)
def handle_response_error(
    request: Request,
    error: OllamaResponseError,
) -> JSONResponse:
    """Handle Ollama response error.
    Args:
        request (Request): FastAPI request.
        error (OllamaResponseError): Raised exception."""
    response_data = JSONResponse(
        status_code=502,
        content={'detail': str(error)},
    )
    return response_data


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
