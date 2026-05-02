from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_root() -> None:
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"message": "Hello from ollama-text-gateway"}


def test_health() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_health_ollama_success(monkeypatch) -> None:
    async def mock_check_ollama_health() -> dict[str, str]:
        return {"status": "ok"}

    monkeypatch.setattr(
        "app.routers.health.check_ollama_health", mock_check_ollama_health)

    response = client.get("/health/ollama")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_health_db_success(monkeypatch) -> None:
    async def mock_check_database() -> bool:
        return True

    monkeypatch.setattr(
        'app.routers.health.check_database',
        mock_check_database,
    )

    response = client.get('/health/db')

    assert response.status_code == 200
    assert response.json() == {'status': 'ok', 'database': 'reachable'}
