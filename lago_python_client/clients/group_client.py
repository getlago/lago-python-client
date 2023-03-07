import requests
from typing import ClassVar, Type

from pydantic import BaseModel
from .base_client import BaseClient
from lago_python_client.models.group import GroupResponse
from requests import Response
from ..services.json import from_json
from ..services.request import make_url
from ..services.response import verify_response


class GroupClient(BaseClient):
    API_RESOURCE: ClassVar[str] = 'groups'
    RESPONSE_MODEL: ClassVar[Type[BaseModel]] = GroupResponse
    ROOT_NAME: ClassVar[str] = 'group'

    def find_all(self, metric_code: str, options: dict = {}):
        query_url: str = make_url(
            scheme_plus_authority=self.base_url,
            path_parts=('billable_metrics', metric_code, self.API_RESOURCE),
            query_pairs=options,
        )
        api_response = requests.get(query_url, headers=self.headers())
        data = from_json(verify_response(api_response))

        return self.prepare_index_response(data)
