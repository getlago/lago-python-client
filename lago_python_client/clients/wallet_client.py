from typing import ClassVar, Dict

from .base_client import BaseClient
from lago_python_client.models.wallet import WalletResponse


class WalletClient(BaseClient):
    API_RESOURCE: ClassVar[str] = 'wallets'
    ROOT_NAME: ClassVar[str] = 'wallet'

    def prepare_response(self, data: Dict):
        return WalletResponse.parse_obj(data)
