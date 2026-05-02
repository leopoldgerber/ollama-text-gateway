from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_models_success(monkeypatch) -> None:
    async def mock_get_models() -> dict[str, list[dict[str, str]]]:
        return {"models": [{"name": "gemma3:270m"}]}

    monkeypatch.setattr("app.routers.ollama.get_models", mock_get_models)

    response = client.get("/models")

    assert response.status_code == 200
    assert response.json() == {"models": [{"name": "gemma3:270m"}]}


def test_generate_success(monkeypatch) -> None:
    async def mock_generate_text(prompt: str) -> dict[str, str]:
        return {
            "response": "test response",
            "model": "gemma3:270m",
        }

    monkeypatch.setattr("app.routers.ollama.generate_text", mock_generate_text)

    response = client.post("/generate", json={"prompt": "Hello"})

    assert response.status_code == 200
    assert response.json() == {
        "response": "test response",
        "model": "gemma3:270m",
    }


def test_generate_empty_prompt() -> None:
    response = client.post("/generate", json={"prompt": ""})

    assert response.status_code == 400
