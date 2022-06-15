from .base_client import BaseClient
from lago_python_client.models.invoice import InvoiceResponse
from typing import Dict


class InvoiceClient(BaseClient):
    def api_resource(self):
        return 'invoices'

    def root_name(self):
        return 'invoice'

    def prepare_response(self, data: Dict):
        return InvoiceResponse.parse_obj(data)
