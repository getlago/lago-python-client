from .base_client import BaseClient


class CustomerClient(BaseClient):
    def api_resource(self):
        return 'customers'

    def root_name(self):
        return 'customer'
