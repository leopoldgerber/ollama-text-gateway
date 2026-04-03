from pydantic import BaseModel, Field, StrictStr


class GenerateRequest(BaseModel):
    """Describe generate request body.
    Args:
        BaseModel (BaseModel): Pydantic base model."""

    text: StrictStr = Field(min_length=1)


class GenerateResponse(BaseModel):
    """Describe generate response body.
    Args:
        BaseModel (BaseModel): Pydantic base model."""

    answer: str
