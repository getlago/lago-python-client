from abc import ABC, abstractmethod
from typing import Optional, Type

from lago_python_client.base_model import BaseModel
from lago_python_client.services.rate_limit import RateLimitRetryConfig


class BaseClient(ABC):
    """The base class used for each collection client."""

    def __init__(
        self,
        base_url: str,
        api_key: str,
        base_ingest_url: str = "",
        rate_limit_retry_config: Optional[RateLimitRetryConfig] = None,
    ):
        self.base_url = base_url
        self.api_key = api_key
        self.base_ingest_url = base_ingest_url
        self.rate_limit_retry_config = rate_limit_retry_config or RateLimitRetryConfig()

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
