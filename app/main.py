from fastapi import FastAPI
import uvicorn


app = FastAPI(title='Project 1')


@app.post('/generate')
def create_reply() -> dict[str, str]:
    """Return stub response.
    Args:
        None: No arguments."""
    return {'status': 'ok'}


def run_server() -> None:
    """Run HTTP server.
    Args:
        None: No arguments."""
    uvicorn.run('app.main:app', host='0.0.0.0', port=8000, reload=True)


if __name__ == '__main__':
    run_server()
