import os

import pytest
from fastapi.testclient import TestClient


from app.main import app


def build_client() -> TestClient:
    """Create test client.
    Args:
        None: No arguments."""
    client = TestClient(app)
    return client


def check_status(response: object, status_code: int) -> object:
    """Check response status code.
    Args:
        response (object): HTTP response object.
        status_code (int): Expected status code."""
    if response.status_code != status_code:
        pytest.fail(
            f'Expected status code {status_code}, '
            f'got {response.status_code}. '
            f'Response body: {response.text}'
        )
    return response


def check_field(data: dict, field_name: str) -> dict:
    """Check response field existence.
    Args:
        data (dict): Response body.
        field_name (str): Required field name."""
    if field_name not in data:
        pytest.fail(f'Missing field: {field_name}. Response body: {data}')
    return data


def check_env_ready(env_name: str) -> str:
    """Check required environment variable.
    Args:
        env_name (str): Environment variable name."""
    env_value = os.getenv(env_name)
    if not env_value:
        pytest.skip(f'Missing environment variable: {env_name}')
    return env_value


@pytest.mark.integration
def test_generate_full_flow() -> None:
    """Test full request flow with real Ollama.
    Args:
        None: No arguments."""
    check_env_ready(env_name='OLLAMA_API_KEY')
    check_env_ready(env_name='OLLAMA_BASE_URL')

    client = build_client()
    response = client.post(
        '/generate',
        json={'text': 'Reply with one short greeting.'},
    )
    checked_response = check_status(response=response, status_code=200)

    response_data = checked_response.json()
    checked_data = check_field(data=response_data, field_name='answer')

    answer_text = checked_data['answer']
    if not isinstance(answer_text, str):
        pytest.fail('Answer must be a string.')

    if not answer_text.strip():
        pytest.fail('Answer must not be empty.')

    return None
