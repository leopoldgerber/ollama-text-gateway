from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
import uvicorn

from app.exceptions import OllamaConnectionError, OllamaResponseError
from app.ollama_client import generate_text
from app.prompt_builder import build_prompt
from app.schemas import GenerateRequest, GenerateResponse


app = FastAPI(title='Ollama Text Gateway')


def build_error_item(error_data: dict) -> dict[str, str]:
    """Build validation error item.
    Args:
        error_data (dict): Validation error data."""
    location_data = error_data.get('loc', [])
    location_text = ' -> '.join(str(item) for item in location_data)
    message_text = str(error_data.get('msg', 'Validation error'))

    error_item = {
        'field': location_text,
        'message': message_text,
    }
    return error_item


def build_error_list(error_items: list[dict]) -> list[dict[str, str]]:
    """Build validation error list.
    Args:
        error_items (list[dict]): Raw validation errors."""
    normalized_errors = [
        build_error_item(error_data=error_data)
        for error_data in error_items
    ]
    return normalized_errors


@app.exception_handler(RequestValidationError)
def handle_validation_error(
    request: Request,
    error: RequestValidationError,
) -> JSONResponse:
    """Handle request validation error.
    Args:
        request (Request): FastAPI request.
        error (RequestValidationError): Raised exception."""
    error_list = build_error_list(error_items=error.errors())
    response_data = JSONResponse(
        status_code=422,
        content={
            'detail': 'Request validation failed.',
            'errors': error_list,
        },
    )
    return response_data


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
