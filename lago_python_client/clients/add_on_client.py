from typing import ClassVar, Type

from pydantic import BaseModel
from .base_client import BaseClient
from ..models.add_on import AddOnResponse


class AddOnClient(BaseClient):
    API_RESOURCE: ClassVar[str] = 'add_ons'
    RESPONSE_MODEL: ClassVar[Type[BaseModel]] = AddOnResponse
    ROOT_NAME: ClassVar[str] = 'add_on'
