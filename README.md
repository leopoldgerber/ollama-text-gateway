# Ollama Text Gateway

A production-like FastAPI service that exposes a small HTTP API for text generation through Ollama.

The project is designed as a practical backend service with containerized deployment, GitLab CI/CD, reverse proxying through Nginx, PostgreSQL connectivity checks, Alembic migration support, and a VPS-based runtime environment.

## Overview

`ollama-text-gateway` is a lightweight API layer between a client and a locally hosted Ollama instance.

Current request flow:

```text
Client -> Nginx -> FastAPI -> Ollama
```

The application runs in Docker, is deployed through GitLab CI/CD, and uses separate Ollama and PostgreSQL containers connected through a shared Docker network.

## Tech Stack

- FastAPI
- Python 3.11
- Ollama
- PostgreSQL
- SQLAlchemy
- Alembic
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
- `GET /health/db` for PostgreSQL reachability checks
- `GET /models` for available Ollama models
- Dockerized application runtime
- Nginx reverse proxy
- GitLab CI pipeline with lint, test, build, infra, and deploy stages
- Docker image publishing to GitLab Container Registry
- SSH-based deploy to VPS
- Separate infrastructure deploy jobs for Ollama and PostgreSQL
- Alembic migration job after application deploy
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
```

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

### `GET /health/db`

Checks whether PostgreSQL is reachable from the application.

Example response:

```json
{
  "status": "ok",
  "database": "reachable"
}
```

If the database is unavailable, the endpoint returns:

```json
{
  "status": "error",
  "database": "unreachable"
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

- empty prompt returns `400`
- prompt made only of spaces returns `400`
- Ollama request failure returns `502`
- response includes both generated text and model name

## Project Structure

```text
.
├── app/
│   ├── db/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── db.py
│   │   ├── models.py
│   │   └── session.py
│   ├── routers/
│   │   ├── health.py
│   │   └── ollama.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── ollama.py
│   │   └── request_statuses.py
│   ├── config.py
│   ├── main.py
│   └── schemas.py
├── alembic/
│   ├── env.py
│   ├── README
│   └── script.py.mako
├── infra/
│   ├── docker-compose.ollama.yml
│   └── docker-compose.postgres.yml
├── tests/
│   ├── test_health.py
│   └── test_ollama.py
├── .gitlab/
│   └── ci/
│       ├── alembic.yml
│       ├── app.yml
│       ├── ollama.yml
│       └── postgres.yml
├── .dockerignore
├── .gitignore
├── .gitlab-ci.yml
├── alembic.ini
├── Dockerfile
├── docker-compose.postgres.local.yml
├── docker-compose.yml
├── Makefile
├── pyproject.toml
├── requirements.txt
└── README.md
```

## Main Modules

- `app/main.py` - FastAPI application initialization and router registration
- `app/config.py` - environment-based configuration
- `app/schemas.py` - request and response schemas
- `app/routers/health.py` - health check endpoints
- `app/routers/ollama.py` - Ollama-related API endpoints
- `app/services/ollama.py` - Ollama integration logic
- `app/db/session.py` - async SQLAlchemy engine and session setup
- `app/db/db.py` - database health check logic
- `alembic/` - database migration setup
- `tests/test_health.py` - health endpoint tests
- `tests/test_ollama.py` - Ollama endpoint tests

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

## Database

The project includes async SQLAlchemy configuration, PostgreSQL health checks, and Alembic migration support.

Current database usage is limited to connectivity checks and migration infrastructure.

### Start local PostgreSQL

```bash
make up-local-db
```

This command starts `docker-compose.postgres.local.yml`, which exposes PostgreSQL on `127.0.0.1:5432` with the default local connection settings.

### Stop local PostgreSQL

```bash
make down-local-db
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

- app exposed on `127.0.0.1:8000`
- `OLLAMA_BASE_URL=http://ollama:11434`
- `OLLAMA_MODEL=gemma3:270m`
- `DATABASE_URL` loaded from the deploy environment
- `ALEMBIC_DATABASE_URL` loaded from the deploy environment
- Docker healthcheck on `/health`
- connection to the external Docker network `ai-backend`

## Environment Variables

| Variable | Purpose | Default / Example |
| --- | --- | --- |
| `OLLAMA_BASE_URL` | Base URL of the Ollama service | `http://ollama:11434` |
| `OLLAMA_MODEL` | Model used for text generation | `gemma3:270m` |
| `DATABASE_URL` | Async SQLAlchemy database URL | `postgresql+asyncpg://postgres:postgres@localhost:5432/postgres` |
| `ALEMBIC_DATABASE_URL` | Sync database URL used by Alembic | `postgresql://postgres:postgres@localhost:5432/postgres` |
| `LLM_TIMEOUT_SECONDS` | Config value reserved for LLM timeout settings | `60` |

## Deployment

The project is deployed through GitLab CI/CD.

Current pipeline stages:

- lint
- test
- build
- infra
- deploy

Main flow:

1. Push to `main`
2. Run `ruff`
3. Run `pytest`
4. Build Docker image
5. Push image to GitLab Container Registry
6. Deploy infrastructure compose files when related files change
7. Deploy the application to VPS over SSH
8. Copy the current `docker-compose.yml` to the server
9. Pull the updated image and restart the app container
10. Run Alembic migrations with `alembic upgrade head`

## Infrastructure Notes

Current production-like setup includes:

- VPS with a dedicated `deploy` user
- Docker and Docker Compose
- Nginx as reverse proxy
- app container bound to `127.0.0.1:8000`
- separate Ollama container
- separate PostgreSQL container
- shared Docker network between app, Ollama, and PostgreSQL
- Uptime Kuma for external health monitoring
- Portainer for container management

The application image and `docker-compose.yml` are updated automatically through CI/CD. Infrastructure compose files for Ollama and PostgreSQL are deployed only when their related files change.

## Monitoring

The service provides:

- `GET /health` for app health
- `GET /health/ollama` for Ollama reachability
- `GET /health/db` for PostgreSQL reachability
- Docker `healthcheck`
- external monitoring through Uptime Kuma

## Current Model

The current model used on the VPS is:

```text
gemma3:270m
```

This model was selected because larger models did not fit the available server RAM.

## Example Requests

### Health

```bash
curl http://127.0.0.1:8000/health
```

### Ollama Health

```bash
curl http://127.0.0.1:8000/health/ollama
```

### Database Health

```bash
curl http://127.0.0.1:8000/health/db
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

- stricter request validation
- better structured error responses
- configurable generation parameters
- using `LLM_TIMEOUT_SECONDS` in the Ollama service
- logging
- request retries
- authentication
- richer tests
- safer deployment workflow
- domain and HTTPS setup

## License

MIT
