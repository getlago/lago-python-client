from typing import ClassVar, Dict, Type

from pydantic import BaseModel
from .base_client import BaseClient
from lago_python_client.models.wallet import WalletResponse


class WalletClient(BaseClient):
    API_RESOURCE: ClassVar[str] = 'wallets'
    RESPONSE_MODEL: ClassVar[Type[BaseModel]] = WalletResponse
    ROOT_NAME: ClassVar[str] = 'wallet'

    def prepare_response(self, data: Dict):
        return self.RESPONSE_MODEL.parse_obj(data)
