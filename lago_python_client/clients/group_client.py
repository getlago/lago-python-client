import requests
from typing import Any, ClassVar, Dict, Type

from pydantic import BaseModel
from .base_client import BaseClient
from lago_python_client.models.group import GroupResponse
from urllib.parse import urljoin, urlencode
from requests import Response
from ..services.json import from_json
from ..services.response import verify_response


class GroupClient(BaseClient):
    API_RESOURCE: ClassVar[str] = 'groups'
    RESPONSE_MODEL: ClassVar[Type[BaseModel]] = GroupResponse
    ROOT_NAME: ClassVar[str] = 'group'

    def prepare_response(self, data: Dict[Any, Any]) -> BaseModel:
        return self.RESPONSE_MODEL.parse_obj(data)

    def find_all(self, metric_code: str, options: dict = {}):
        uri: str = '{uri_path}{uri_query}'.format(
            uri_path='/'.join(('billable_metrics', metric_code, self.API_RESOURCE)),
            uri_query=f'?{urlencode(options)}' if options else '',
        )
        query_url: str = urljoin(self.base_url, uri)

        api_response = requests.get(query_url, headers=self.headers())
        data = from_json(verify_response(api_response))

        return self.prepare_index_response(data)
