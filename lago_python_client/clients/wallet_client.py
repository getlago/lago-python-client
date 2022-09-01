from .base_client import BaseClient
from lago_python_client.models.wallet import WalletResponse
from typing import Dict


class WalletClient(BaseClient):
    def api_resource(self):
        return 'wallets'

    def root_name(self):
        return 'wallet'

    def prepare_response(self, data: Dict):
        return WalletResponse.parse_obj(data)
