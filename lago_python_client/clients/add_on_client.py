from typing import Any, ClassVar, Dict, Type

from pydantic import BaseModel
from .base_client import BaseClient
from lago_python_client.models.add_on import AddOnResponse


class AddOnClient(BaseClient):
    API_RESOURCE: ClassVar[str] = 'add_ons'
    RESPONSE_MODEL: ClassVar[Type[BaseModel]] = AddOnResponse
    ROOT_NAME: ClassVar[str] = 'add_on'

    @classmethod
    def prepare_response(cls, data: Dict[Any, Any]) -> BaseModel:
        return cls.RESPONSE_MODEL.parse_obj(data)
