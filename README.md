# Ollama Text Gateway

HTTP API service that validates input, builds prompts, sends requests to Ollama, and returns generated text responses.

## Overview

Ollama Text Gateway is a small FastAPI-based backend service that exposes a single `POST /generate` endpoint.

The service accepts user text, validates the request body, inserts the text into a prompt template, sends the prompt to Ollama, and returns the generated answer as JSON.

This project is intentionally simple and focused on the core request flow:

request → validation → prompt building → Ollama call → response

---

## Features

- FastAPI HTTP server
- `POST /generate` endpoint
- JSON request/response schema
- input validation for `text`
- prompt template assembly in a dedicated function
- Ollama API integration
- structured error handling
- unit tests with `pytest`
- integration test for full end-to-end flow
- `Makefile` commands for common tasks

---

## Request Flow

1. Client sends a `POST /generate` request
2. The server validates the JSON body
3. The application builds a prompt from the user input
4. The prompt is sent to Ollama
5. The model response is extracted
6. The API returns a JSON response with the generated answer

---

## Tech Stack

- Python 3.11+
- FastAPI
- Uvicorn
- HTTPX
- python-dotenv
- pytest

---

## Project Structure

```text
.
├── app/
│   ├── exceptions.py
│   ├── main.py
│   ├── ollama_client.py
│   ├── prompt_builder.py
│   ├── prompts.py
│   └── schemas.py
├── tests/
│   ├── test_integration.py
│   └── test_main.py
├── .env.example
├── Makefile
├── pyproject.toml
└── LICENSE
````

### Main modules

* `app/main.py` — FastAPI app, route definition, exception handlers
* `app/schemas.py` — request and response schemas
* `app/prompt_builder.py` — prompt construction logic
* `app/prompts.py` — prompt template definition
* `app/ollama_client.py` — Ollama API client and response extraction
* `app/exceptions.py` — custom exception types
* `tests/test_main.py` — unit tests for endpoint behavior
* `tests/test_integration.py` — integration test for real Ollama flow

---

## API

### `POST /generate`

Generate a response from the model based on input text.

#### Request body

```json
{
  "text": "Hello, world"
}
```

#### Successful response

```json
{
  "answer": "Model response text"
}
```

---

## Validation Rules

The `text` field must:

* exist in the request body
* be a string
* not be empty

If validation fails, the service returns a `422` response with structured error details.

Example shape:

```json
{
  "detail": "Request validation failed.",
  "errors": [
    {
      "field": "body -> text",
      "message": "Field required"
    }
  ]
}
```

---

## Error Handling

The service handles the following error groups:

* request validation errors
* Ollama connection errors
* invalid Ollama JSON responses
* empty or malformed model responses

Connection and upstream response problems are returned as `502 Bad Gateway`.

---

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/leopoldgerber/ollama-text-gateway.git
cd ollama-text-gateway
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv
```

#### Linux / macOS

```bash
source .venv/bin/activate
```

#### Windows PowerShell

```bash
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -e .
```

For development tools:

```bash
pip install -e .[dev]
```

---

## Environment Variables

Create a `.env` file based on `.env.example`.

Required variables:

* `OLLAMA_API_KEY`
* `OLLAMA_BASE_URL`

Example:

```env
OLLAMA_API_KEY=your_api_key_here
OLLAMA_BASE_URL=https://ollama.com
```

---

## Running the Server

You can start the application with the `Makefile`:

```bash
make run-server
```

This runs:

```bash
python app/main.py
```

By default, the server starts on:

```text
http://localhost:8000
```

---

## Running Tests

This project uses `pytest`.

### Unit tests

```bash
make run-tests
```

or:

```bash
pytest
```

### Integration test

The integration test performs a real full-flow request against Ollama.

Run it with:

```bash
make run-integration-tests
```

or:

```bash
pytest -m integration
```

### Notes about integration testing

Integration tests require:

* `OLLAMA_API_KEY`
* `OLLAMA_BASE_URL`

If these variables are missing, the integration test is skipped.

---

## Makefile Commands

The project includes a simple `Makefile` for common commands:

```bash
make run-server
make run-tests
make run-integration-tests
```

### Available targets

* `run-server` — start the FastAPI server
* `run-tests` — run all tests with `pytest`
* `run-integration-tests` — run integration tests marked with `integration`

---

## Example Request

Using `curl`:

```bash
curl -X POST http://localhost:8000/generate \
  -H "Content-Type: application/json" \
  -d '{"text":"Reply with one short greeting."}'
```

Example response:

```json
{
  "answer": "Hello!"
}
```

---

## Implementation Scope

This project covers the following implementation stages:

1. Base HTTP server
2. Request/response schema
3. Input validation
4. Prompt building
5. Ollama integration
6. Response formatting
7. Error handling
8. Basic testing

---

## Development Notes

This repository is designed as a compact backend exercise around a typical LLM application flow:

* accept text input
* validate request data
* assemble prompt context
* call model provider
* normalize output
* return API response
* verify behavior with tests

It is a good base for extending into a more production-oriented service with:

* config management
* logging
* retries/timeouts
* Docker support
* CI pipeline
* stricter test coverage
* health endpoints
* model selection and request options

---

## License

This project is distributed under the terms of the license included in this repository.
