import base64
import requests
from typing import ClassVar, Type

from pydantic import BaseModel
from .base_client import BaseClient
from ..services.json import from_json
from ..services.request import make_url
from ..services.response import verify_response


class WebhookClient(BaseClient):
    API_RESOURCE: ClassVar[str] = 'webhooks'
    RESPONSE_MODEL: ClassVar[Type[BaseModel]] = NotImplemented
    ROOT_NAME: ClassVar[str] = 'webhook'

    def public_key(self):
        query_url: str = make_url(
            scheme_plus_authority=self.base_url,
            path_parts=(self.API_RESOURCE, 'json_public_key'),
        )
        api_response = requests.get(query_url, headers=self.headers())
        data = from_json(verify_response(api_response)).get(self.ROOT_NAME)

        return base64.b64decode(data['public_key'])
