from pydantic import BaseModel


class BaseResponseModel(BaseModel):
    """Base class for response model."""

    class Config:
        frozen = True
