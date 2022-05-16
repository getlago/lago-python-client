import requests

from urllib.parse import urljoin
from .base_client import BaseClient


class WebhookClient(BaseClient):
    def public_key(self):
        query_url = urljoin(self.base_url, 'webhooks/public_key')

        api_response = requests.get(query_url, headers=self.headers())

        return self.handle_response(api_response).text

    def headers(self):
        bearer = "Bearer " + self.api_key
        headers = {'Authorization': bearer}

        return headers
