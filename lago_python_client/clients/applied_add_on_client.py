from typing import ClassVar, Type

from pydantic import BaseModel

from .base_client import BaseClient
from ..models.applied_add_on import AppliedAddOnResponse


class AppliedAddOnClient(BaseClient):
    API_RESOURCE: ClassVar[str] = 'applied_add_ons'
    RESPONSE_MODEL: ClassVar[Type[BaseModel]] = AppliedAddOnResponse
    ROOT_NAME: ClassVar[str] = 'applied_add_on'
