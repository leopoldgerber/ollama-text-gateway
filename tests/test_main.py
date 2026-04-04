import pytest
from fastapi.testclient import TestClient


from app.main import app


def build_client() -> TestClient:
    """Create test client.
    Args:
        None: No arguments."""
    client = TestClient(app)
    return client


def check_status(response, status_code: int) -> object:
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


def fake_generate(prompt_text: str) -> str:
    """Return fake model response.
    Args:
        prompt_text (str): Prompt text."""
    if not isinstance(prompt_text, str):
        pytest.fail('Prompt text must be a string.')
    return 'Mocked answer'


def test_generate_valid(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test valid generate request.
    Args:
        monkeypatch (pytest.MonkeyPatch): Pytest monkeypatch fixture."""
    monkeypatch.setattr('app.main.generate_text', fake_generate)

    client = build_client()
    response = client.post('/generate', json={'text': 'Hello'})
    checked_response = check_status(response=response, status_code=200)

    response_data = checked_response.json()
    checked_data = check_field(data=response_data, field_name='answer')

    if checked_data['answer'] != 'Mocked answer':
        pytest.fail(
            f"Expected 'Mocked answer', got {checked_data['answer']}"
        )

    return None


def test_generate_missing_text() -> None:
    """Test request without text field.
    Args:
        None: No arguments."""
    client = build_client()
    response = client.post('/generate', json={})
    checked_response = check_status(response=response, status_code=422)

    response_data = checked_response.json()
    checked_data = check_field(data=response_data, field_name='detail')
    checked_data = check_field(data=checked_data, field_name='errors')

    if not isinstance(checked_data['errors'], list):
        pytest.fail('Validation errors must be a list.')

    return None


def test_generate_invalid_text() -> None:
    """Test request with invalid text type.
    Args:
        None: No arguments."""
    client = build_client()
    response = client.post('/generate', json={'text': 123})
    checked_response = check_status(response=response, status_code=422)

    response_data = checked_response.json()
    checked_data = check_field(data=response_data, field_name='detail')
    checked_data = check_field(data=checked_data, field_name='errors')

    if not isinstance(checked_data['errors'], list):
        pytest.fail('Validation errors must be a list.')

    return None