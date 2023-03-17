import requests
import sys
from typing import Any, ClassVar, Type

from pydantic import BaseModel
from requests import Response

from .base_client import BaseClient
from ..models.group import GroupResponse
from ..services.json import from_json
from ..services.request import make_url
from ..services.response import prepare_index_response, verify_response

if sys.version_info >= (3, 9):
    from collections.abc import Mapping
else:
    from typing import Mapping


class GroupClient(BaseClient):
    API_RESOURCE: ClassVar[str] = 'groups'
    RESPONSE_MODEL: ClassVar[Type[BaseModel]] = GroupResponse
    ROOT_NAME: ClassVar[str] = 'group'

    def find_all(self, metric_code: str, options: dict = {}) -> Mapping[str, Any]:
        query_url: str = make_url(
            origin=self.base_url,
            path_parts=('billable_metrics', metric_code, self.API_RESOURCE),
            query_pairs=options,
        )
        api_response: Response = requests.get(query_url, headers=self.headers())

        return prepare_index_response(
            api_resource=self.API_RESOURCE,
            response_model=self.RESPONSE_MODEL,
            data=from_json(verify_response(api_response)),
        )
