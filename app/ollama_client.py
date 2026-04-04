from typing import Any
import httpx

from app.config import SETTINGS
from app.exceptions import OllamaConnectionError, OllamaResponseError
from app.logger_config import get_logger


logger = get_logger(logger_name='ollama_text_gateway.ollama')


def create_client_config(
    model_name: str = 'gpt-oss:20b-cloud',
) -> dict[str, Any]:
    """Create Ollama client config.
    Args:
        model_name (str): Ollama model name."""
    client_config: dict[str, Any] = {
        'model_name': model_name,
        'base_url': SETTINGS['ollama_base_url'],
        'headers': {
            'Authorization': f"Bearer {SETTINGS['ollama_api_key']}",
            'Content-Type': 'application/json',
        },
    }
    return client_config


def build_payload(prompt_text: str, model_name: str) -> dict[str, Any]:
    """Build chat payload.
    Args:
        prompt_text (str): Prompt text.
        model_name (str): Ollama model name."""
    payload: dict[str, Any] = {
        'model': model_name,
        'messages': [{'role': 'user', 'content': prompt_text}],
        'stream': False,
    }
    return payload


def call_ollama(
    client_config: dict[str, Any],
    payload: dict[str, Any],
) -> dict[str, Any]:
    """Send request to Ollama API.
    Args:
        client_config (dict[str, Any]): Client configuration.
        payload (dict[str, Any]): Request payload."""
    api_url = f"{client_config['base_url'].rstrip('/')}/api/chat"

    logger.info('Calling Ollama API.')

    try:
        with httpx.Client(timeout=30.0) as client:
            response = client.post(
                api_url,
                headers=client_config['headers'],
                json=payload,
            )
            response.raise_for_status()
            response_data = response.json()
    except httpx.HTTPError as error:
        logger.error('Ollama connection failed: %s', str(error))
        raise OllamaConnectionError('Failed to connect to Ollama.') from error
    except ValueError as error:
        logger.error('Ollama returned invalid JSON: %s', str(error))
        raise OllamaResponseError('Ollama returned invalid JSON.') from error

    logger.info('Ollama API returned response.')
    return response_data


def fetch_reply(response_data: dict[str, Any]) -> str:
    """Extract reply text.
    Args:
        response_data (dict[str, Any]): Ollama response data."""
    message_data = response_data.get('message')
    if not isinstance(message_data, dict):
        logger.error('Ollama response does not contain message object.')
        raise OllamaResponseError(
            'Ollama response must contain message object.'
        )

    response_text = message_data.get('content')
    if not isinstance(response_text, str):
        logger.error('Ollama response content is not a string.')
        raise OllamaResponseError(
            'Ollama response must contain string message content.'
        )

    if not response_text.strip():
        logger.error('Ollama response content is empty.')
        raise OllamaResponseError('Ollama response content is empty.')

    return response_text


def generate_text(prompt_text: str) -> str:
    """Generate text with Ollama.
    Args:
        prompt_text (str): Prompt text."""
    logger.info('Generating text with Ollama.')

    client_config = create_client_config(
        model_name=SETTINGS['ollama_model_name']
    )
    payload = build_payload(
        prompt_text=prompt_text,
        model_name=client_config['model_name'],
    )
    response_data = call_ollama(
        client_config=client_config,
        payload=payload,
    )
    response_text = fetch_reply(response_data=response_data)

    logger.info('Text generation completed.')
    return response_text


if __name__ == '__main__':
    result_text = generate_text(prompt_text='Say hello.')
    print(result_text)
