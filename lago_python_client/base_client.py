from abc import ABC
from typing import Any, ClassVar, Optional, Type

from lago_python_client.services.rate_limit import RateLimitRetryConfig


class BaseClient(ABC):
    """The base class used for each collection client."""

    API_RESOURCE: ClassVar[str]
    RESPONSE_MODEL: ClassVar[Type[Any]]
    ROOT_NAME: ClassVar[str]

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
