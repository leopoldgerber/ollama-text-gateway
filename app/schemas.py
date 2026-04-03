from pydantic import BaseModel


class GenerateRequest(BaseModel):
    """Describe generate request body.
    Args:
        BaseModel (BaseModel): Pydantic base model."""

    text: str


class GenerateResponse(BaseModel):
    """Describe generate response body.
    Args:
        BaseModel (BaseModel): Pydantic base model."""

    answer: str
