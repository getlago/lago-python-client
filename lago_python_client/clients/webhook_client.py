import base64
import requests

from urllib.parse import urljoin
from .base_client import BaseClient
from ..services.json import from_json


class WebhookClient(BaseClient):
    def root_name(self):
        return 'webhook'

    def public_key(self):
        query_url = urljoin(self.base_url, 'webhooks/json_public_key')

        api_response = requests.get(query_url, headers=self.headers())
        data = from_json(self.handle_response(api_response)).get(self.root_name())

        return base64.b64decode(data['public_key'])
