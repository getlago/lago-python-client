import base64
import requests

from urllib.parse import urljoin
from .base_client import BaseClient


class WebhookClient(BaseClient):
    def root_name(self):
        return 'webhook'

    def public_key(self):
        query_url = urljoin(self.base_url, 'webhooks/public_key')

        api_response = requests.get(query_url, headers=self.headers())
        data = self.handle_response(api_response).json().get(self.root_name())

        return base64.b64decode(data['public_key'])
