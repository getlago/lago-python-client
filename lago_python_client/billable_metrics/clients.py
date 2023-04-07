import sys
from typing import Any, ClassVar, Type, Union

from ..base_client import BaseClient
from ..mixins import CreateCommandMixin, DestroyCommandMixin, FindAllCommandMixin, FindCommandMixin, UpdateCommandMixin
from ..models.billable_metric import BillableMetricResponse
from ..models.group import GroupResponse
from ..services.request import make_headers, make_url, send_get_request
from ..services.response import get_response_data, prepare_index_response, Response

if sys.version_info >= (3, 9):
    from collections.abc import Mapping
else:
    from typing import Mapping


class BillableMetricClient(
    CreateCommandMixin[BillableMetricResponse],
    DestroyCommandMixin[BillableMetricResponse],
    FindAllCommandMixin[BillableMetricResponse],
    FindCommandMixin[BillableMetricResponse],
    UpdateCommandMixin[BillableMetricResponse],
    BaseClient,
):
    API_RESOURCE: ClassVar[str] = 'billable_metrics'
    RESPONSE_MODEL: ClassVar[Type[BillableMetricResponse]] = BillableMetricResponse
    ROOT_NAME: ClassVar[str] = 'billable_metric'


class GroupClient(BaseClient):
    API_RESOURCE: ClassVar[str] = 'groups'
    RESPONSE_MODEL: ClassVar[Type[GroupResponse]] = GroupResponse
    ROOT_NAME: ClassVar[str] = 'group'

    def find_all(self, metric_code: str, options: Mapping[str, Union[int, str]] = {}) -> Mapping[str, Any]:
        api_response: Response = send_get_request(
            url=make_url(
                origin=self.base_url,
                path_parts=('billable_metrics', metric_code, self.API_RESOURCE),
                query_pairs=options,
            ),
            headers=make_headers(api_key=self.api_key),
        )

        return prepare_index_response(
            api_resource=self.API_RESOURCE,
            response_model=self.RESPONSE_MODEL,
            data=get_response_data(response=api_response),
        )
