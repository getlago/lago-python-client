try:
    from pydantic.v1 import Field, BaseModel as PydanticBaseModel
except ImportError:
    from pydantic import Field, BaseModel as PydanticBaseModel


class BaseModel(PydanticBaseModel):
    """Base class for all models."""

    def to_create_payload(self) -> dict:
        """Convert model to payload dict (for create requests)"""
        return self.dict()

    def to_update_payload(self) -> dict:
        """Convert model to payload dict (for update requests)"""
        return self.dict(exclude_none=True)


class BaseResponseModel(BaseModel):
    """Base class for response model."""

    class Config:
        frozen = True


__all__ = [
    "Field",
    "BaseModel",
    "BaseResponseModel",
]
