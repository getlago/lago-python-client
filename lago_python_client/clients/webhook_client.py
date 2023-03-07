import base64
import requests
from typing import ClassVar, Type

from pydantic import BaseModel
from urllib.parse import urljoin
from .base_client import BaseClient
from ..services.json import from_json
from ..services.response import verify_response


class WebhookClient(BaseClient):
    API_RESOURCE: ClassVar[str] = 'webhooks'
    RESPONSE_MODEL: ClassVar[Type[BaseModel]] = NotImplemented
    ROOT_NAME: ClassVar[str] = 'webhook'

    def public_key(self):
        uri: str = '/'.join((self.API_RESOURCE, 'json_public_key'))
        query_url: str = urljoin(self.base_url, uri)

        api_response = requests.get(query_url, headers=self.headers())
        data = from_json(verify_response(api_response)).get(self.ROOT_NAME)

        return base64.b64decode(data['public_key'])
