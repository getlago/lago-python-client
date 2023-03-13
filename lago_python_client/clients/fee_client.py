import requests
from typing import Any, ClassVar, Type

from pydantic import BaseModel
from .base_client import BaseClient
from lago_python_client.models.fee import FeeResponse

class FeeClient(BaseClient):
    API_RESOURCE: ClassVar[str] = 'fees'
    RESPONSE_MODEL: ClassVar[Type[BaseModel]] = FeeResponse
    ROOT_NAME: ClassVar[str] = 'fee'
