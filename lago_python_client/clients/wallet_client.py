from typing import Any, ClassVar, Dict, Type

from pydantic import BaseModel
from .base_client import BaseClient
from lago_python_client.models.wallet import WalletResponse


class WalletClient(BaseClient):
    API_RESOURCE: ClassVar[str] = 'wallets'
    RESPONSE_MODEL: ClassVar[Type[BaseModel]] = WalletResponse
    ROOT_NAME: ClassVar[str] = 'wallet'

    @classmethod
    def prepare_object_response(cls, data: Dict[Any, Any]) -> BaseModel:
        return cls.RESPONSE_MODEL.parse_obj(data)
