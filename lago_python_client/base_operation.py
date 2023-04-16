from abc import ABC, abstractmethod
from typing import Type

from pydantic import BaseModel


class BaseOperation(ABC):
    """The base class used for each OpenAPI-based operation."""

    def __init__(self, base_url: str, api_key: str):
        self.base_url: str = base_url
        self.api_key: str = api_key

    @property
    @classmethod
    @abstractmethod
    def API_RESOURCE(cls) -> str:
        """Collection name (required class property) used to build query urls."""
        raise NotImplementedError

    @property
    @classmethod
    @abstractmethod
    def RESPONSE_MODEL(cls) -> Type[BaseModel]:
        """Response model (required class property) used to prepare response."""
        raise NotImplementedError

    @property
    @classmethod
    @abstractmethod
    def ROOT_NAME(cls) -> str:
        """The resource key (required class property), used to access the response data."""
        raise NotImplementedError
