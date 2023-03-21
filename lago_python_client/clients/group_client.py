import requests
import sys
from typing import Any, ClassVar, Type

from requests import Response

from .base_client import BaseClient
from ..mixins import CreateCommandMixin, DestroyCommandMixin, FindCommandMixin, UpdateCommandMixin
from ..models.group import GroupResponse
from ..services.request import make_url
from ..services.response import get_response_data, prepare_index_response

if sys.version_info >= (3, 9):
    from collections.abc import Mapping
else:
    from typing import Mapping


class GroupClient(
    CreateCommandMixin[GroupResponse],
    DestroyCommandMixin[GroupResponse],
    FindCommandMixin[GroupResponse],
    UpdateCommandMixin[GroupResponse],
    BaseClient,
):
    API_RESOURCE: ClassVar[str] = 'groups'
    RESPONSE_MODEL: ClassVar[Type[GroupResponse]] = GroupResponse
    ROOT_NAME: ClassVar[str] = 'group'

    def find_all(self, metric_code: str, options: Mapping[str, str] = {}) -> Mapping[str, Any]:
        api_response: Response = requests.get(
            url=make_url(
                origin=self.base_url,
                path_parts=('billable_metrics', metric_code, self.API_RESOURCE),
                query_pairs=options,
            ),
            headers=self.headers(),
        )

        return prepare_index_response(
            api_resource=self.API_RESOURCE,
            response_model=self.RESPONSE_MODEL,
            data=get_response_data(response=api_response),
        )
