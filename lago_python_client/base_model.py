try:
    from pydantic.v1 import BaseModel  # type: ignore
except ImportError:
    from pydantic import BaseModel


class BaseResponseModel(BaseModel):
    """Base class for response model."""

    class Config:
        frozen = True
