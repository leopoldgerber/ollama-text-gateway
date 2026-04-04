import time
from typing import Any

from fastapi import FastAPI
from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.responses import Response
import uvicorn

from app.config import SETTINGS
from app.exceptions import OllamaConnectionError
from app.exceptions import OllamaResponseError
from app.logger_config import get_logger
from app.metrics import get_metrics
from app.metrics import get_metrics_output
from app.metrics import get_metrics_type
from app.metrics import increment_errors
from app.metrics import increment_requests
from app.metrics import save_response_time
from app.metrics import update_health
from app.ollama_client import generate_text
from app.prompt_builder import build_prompt
from app.schemas import GenerateRequest
from app.schemas import GenerateResponse


app = FastAPI(title=SETTINGS['app_title'])
logger = get_logger(logger_name='ollama_text_gateway.app')


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
    increment_errors(error_type='validation_errors_total')
    logger.error(
        'Validation error. Path: %s. Errors: %s',
        request.url.path,
        error.errors(),
    )
    response_data = JSONResponse(
        status_code=422,
        content={
            'detail': 'Request validation failed.',
            'errors': build_error_list(error_items=error.errors()),
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
    increment_errors(error_type='ollama_connection_errors_total')
    logger.error(
        'Ollama connection error. Path: %s. Error: %s',
        request.url.path,
        str(error),
    )
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
    increment_errors(error_type='ollama_response_errors_total')
    logger.error(
        'Ollama response error. Path: %s. Error: %s',
        request.url.path,
        str(error),
    )
    response_data = JSONResponse(
        status_code=502,
        content={'detail': str(error)},
    )
    return response_data


@app.get('/health')
def check_health() -> dict[str, str]:
    """Return service health status.
    Args:
        None: No arguments."""
    logger.info('Received request on /health.')
    update_health(status_value=1)
    response_data = {'status': 'ok'}
    return response_data


@app.get('/metrics')
def show_metrics() -> Response:
    """Return Prometheus metrics.
    Args:
        None: No arguments."""
    logger.info('Received request on /metrics.')
    metrics_output = get_metrics_output()
    response_data = Response(
        content=metrics_output,
        media_type=get_metrics_type(),
    )
    return response_data


@app.get('/metrics/json')
def show_json_metrics() -> dict[str, Any]:
    """Return JSON metrics.
    Args:
        None: No arguments."""
    logger.info('Received request on /metrics/json.')
    metrics_data = get_metrics()
    return metrics_data


@app.post('/generate', response_model=GenerateResponse)
def create_reply(request_data: GenerateRequest) -> GenerateResponse:
    """Generate model response.
    Args:
        request_data (GenerateRequest): Request body data."""
    logger.info('Received request on /generate.')

    start_time = time.perf_counter()

    increment_requests(endpoint='/generate')
    prompt_text = build_prompt(user_text=request_data.text)
    answer_text = generate_text(prompt_text=prompt_text)
    response_data = GenerateResponse(answer=answer_text)

    response_time = time.perf_counter() - start_time
    save_response_time(
        endpoint='/generate',
        response_time=response_time,
    )

    logger.info(
        'Request on /generate completed successfully. '
        'Response time: %.4f sec.',
        response_time,
    )
    return response_data


def run_server() -> None:
    """Run HTTP server.
    Args:
        None: No arguments."""
    uvicorn.run(
        'app.main:app',
        host=SETTINGS['app_host'],
        port=int(SETTINGS['app_port']),
        reload=SETTINGS['app_reload'].lower() == 'true',
    )


if __name__ == '__main__':
    run_server()
