from fastapi import FastAPI
import uvicorn


from app.schemas import GenerateRequest, GenerateResponse


app = FastAPI(title='Project 1')


@app.post('/generate', response_model=GenerateResponse)
def create_reply(request_data: GenerateRequest) -> GenerateResponse:
    """Return stub response.
    Args:
        request_data (GenerateRequest): Request body data."""
    return GenerateResponse(answer='Stub response')


def run_server() -> None:
    """Run HTTP server.
    Args:
        None: No arguments."""
    uvicorn.run('app.main:app', host='0.0.0.0', port=8000, reload=True)


if __name__ == '__main__':
    run_server()
