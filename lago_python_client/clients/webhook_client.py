import base64
import requests

from urllib.parse import urljoin
from .base_client import BaseClient


class WebhookClient(BaseClient):
    def public_key(self):
        query_url = urljoin(self.base_url, 'webhooks/public_key')

        api_response = requests.get(query_url, headers=self.headers())
        coded_response = self.handle_response(api_response).text

        return base64.b64decode(coded_response)

    def headers(self):
        bearer = "Bearer " + self.api_key
        headers = {'Authorization': bearer}

        return headers
