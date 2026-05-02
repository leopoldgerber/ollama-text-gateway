# Ollama Text Gateway

A production-like FastAPI service that exposes a small HTTP API for text generation through Ollama.

The project is designed as a practical backend service with containerized deployment, GitLab CI/CD, reverse proxying through Nginx, and a VPS-based runtime environment.

## Overview

`ollama-text-gateway` is a lightweight API layer between a client and a locally hosted Ollama instance.

Current request flow:

Client -> Nginx -> FastAPI -> Ollama

The application runs in Docker, is deployed through GitLab CI/CD, and uses a separate Ollama container connected through a shared Docker network.

## Tech Stack

- FastAPI
- Python 3.11
- Ollama
- Docker
- Docker Compose
- Nginx
- GitLab CI/CD
- Ruff
- Pytest
- VPS (Beget)

## Features

- FastAPI application with a small HTTP API
- `POST /generate` for text generation
- `GET /health` for service health
- `GET /health/ollama` for Ollama reachability checks
- `GET /models` for available Ollama models
- Dockerized application runtime
- Nginx reverse proxy
- GitLab CI pipeline with lint, test, build, and deploy stages
- Docker image publishing to GitLab Container Registry
- SSH-based deploy to VPS
- Docker healthcheck support
- Monitoring with Uptime Kuma
- Container management with Portainer

## Current API

### `GET /`

Returns a basic welcome message.

Example response:

```json
{
  "message": "Hello from ollama-text-gateway"
}
````

### `GET /health`

Returns the application health status.

Example response:

```json
{
  "status": "ok"
}
```

### `GET /health/ollama`

Checks whether Ollama is reachable from the application.

Example response:

```json
{
  "status": "ok",
  "ollama": "reachable"
}
```

### `GET /models`

Returns a list of models available in Ollama.

Example response:

```json
{
  "models": [
    {
      "name": "gemma3:270m",
      "model": "gemma3:270m"
    }
  ]
}
```

### `POST /generate`

Generates text using the model configured in `OLLAMA_MODEL`.

Request body:

```json
{
  "prompt": "Say hello"
}
```

Example response:

```json
{
  "response": "Hello!",
  "model": "gemma3:270m"
}
```

## Validation and Error Handling

Current behavior:

* empty prompt made only of spaces returns `400`
* Ollama request failure returns `502`
* Ollama timeout handling is covered by tests
* response includes both generated text and model name

## Project Structure

```text
.
├── app/
│   ├── config.py
│   ├── main.py
│   ├── schemas.py
│   └── services/
│       ├── __init__.py
│       └── ollama.py
├── tests/
│   └── test_main.py
├── .dockerignore
├── .gitignore
├── .gitlab-ci.yml
├── Dockerfile
├── docker-compose.yml
├── Makefile
├── pyproject.toml
└── README.md
```

## Main Modules

* `app/main.py` - FastAPI app and route handlers
* `app/config.py` - environment-based configuration
* `app/schemas.py` - request and response schemas
* `app/services/ollama.py` - Ollama integration logic
* `tests/test_main.py` - API tests with mocked Ollama requests

## Local Development

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd ollama-text-gateway
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -e .
```

For development dependencies:

```bash
pip install -e .[dev]
```

## Run the Application

This project includes a `Makefile`.

Start the local development server with:

```bash
make run-server
```

Current target:

```bash
uvicorn app.main:app --reload
```

By default, the app runs on:

```text
http://127.0.0.1:8000
```

## Run Tests

This project uses `pytest`.

Run tests with:

```bash
pytest
```

## Linting

This project uses `ruff`.

Run lint locally with:

```bash
ruff check .
```

## Docker

### Build image locally

```bash
docker build -t ollama-text-gateway .
```

### Run with Docker Compose

```bash
docker compose up -d
```

Current runtime configuration includes:

* app exposed on `127.0.0.1:8000`
* `OLLAMA_BASE_URL=http://ollama:11434`
* `OLLAMA_MODEL=gemma3:270m`
* Docker healthcheck on `/health`
* connection to the external Docker network `ai-backend`

## Deployment

The project is deployed through GitLab CI/CD.

Current pipeline stages:

* lint
* test
* build
* deploy

Main flow:

1. Push to `main`
2. Run `ruff`
3. Run `pytest`
4. Build Docker image
5. Push image to GitLab Container Registry
6. Deploy to VPS over SSH
7. Pull updated image and restart the container on the server

## Infrastructure Notes

Current production-like setup includes:

* VPS with a dedicated `deploy` user
* Docker and Docker Compose
* Nginx as reverse proxy
* app container bound to `127.0.0.1:8000`
* separate Ollama container
* shared Docker network between app and Ollama
* Uptime Kuma for external health monitoring
* Portainer for container management

## Monitoring

The service provides:

* `GET /health` for app health
* Docker `healthcheck`
* external monitoring through Uptime Kuma

## Current Model

The current model used on the VPS is:

```text
gemma3:270m
```

This model was selected because larger models did not fit the available server RAM.

## Important Note

The application image is updated automatically through CI/CD, but the server-side `docker-compose.yml` is currently updated manually.

That behavior is intentional for now.

## Example Requests

### Health

```bash
curl http://127.0.0.1:8000/health
```

### Models

```bash
curl http://127.0.0.1:8000/models
```

### Generate

```bash
curl -X POST http://127.0.0.1:8000/generate \
  -H "Content-Type: application/json" \
  -d '{"prompt":"Say hello"}'
```

## Roadmap Direction

The current base is already working and can be extended step by step.

Possible next improvements:

* stricter request validation
* better structured error responses
* configurable generation parameters
* logging
* request timeouts and retries
* authentication
* richer tests
* safer deployment workflow
* domain and HTTPS setup

## License

MIT