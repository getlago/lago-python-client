import sys
from typing import Any, ClassVar, Type, Union

from ..base_operation import BaseOperation
from ..models.billable_metric import BillableMetricResponse
from ..models.group import GroupResponse
from ..services.request import make_headers, make_url, send_get_request
from ..services.response import get_response_data, prepare_index_response, Response
from ..shared_operations import CreateCommandMixin, DestroyCommandMixin, FindAllCommandMixin, FindCommandMixin, UpdateCommandMixin

if sys.version_info >= (3, 9):
    from collections.abc import Callable, Mapping
else:
    from typing import Callable, Mapping


class CreateBillableMetric(CreateCommandMixin[BillableMetricResponse], BaseOperation):
    """Create a new billable metric."""

    API_RESOURCE: ClassVar[str] = 'billable_metrics'
    RESPONSE_MODEL: ClassVar[Type[BillableMetricResponse]] = BillableMetricResponse
    ROOT_NAME: ClassVar[str] = 'billable_metric'


class DestroyBillableMetric(DestroyCommandMixin[BillableMetricResponse], BaseOperation):
    """Delete a billable metric."""

    API_RESOURCE: ClassVar[str] = 'billable_metrics'
    RESPONSE_MODEL: ClassVar[Type[BillableMetricResponse]] = BillableMetricResponse
    ROOT_NAME: ClassVar[str] = 'billable_metric'


class FindAllBillableMetrics(FindAllCommandMixin[BillableMetricResponse], BaseOperation):
    """Find Billable metrics."""

    API_RESOURCE: ClassVar[str] = 'billable_metrics'
    RESPONSE_MODEL: ClassVar[Type[BillableMetricResponse]] = BillableMetricResponse
    ROOT_NAME: ClassVar[str] = 'billable_metric'


class FindAllBillableMetricGroups(BaseOperation):
    """Find Billable metric groups."""

    API_RESOURCE: ClassVar[str] = 'groups'
    RESPONSE_MODEL: ClassVar[Type[GroupResponse]] = GroupResponse
    ROOT_NAME: ClassVar[str] = 'group'

    def __call__(self, metric_code: str, options: Mapping[str, Union[int, str]] = {}) -> Mapping[str, Any]:
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


class FindBillableMetric(FindCommandMixin[BillableMetricResponse], BaseOperation):
    """Find billable metric by code."""

    API_RESOURCE: ClassVar[str] = 'billable_metrics'
    RESPONSE_MODEL: ClassVar[Type[BillableMetricResponse]] = BillableMetricResponse
    ROOT_NAME: ClassVar[str] = 'billable_metric'


class UpdateBillableMetric(UpdateCommandMixin[BillableMetricResponse], BaseOperation):
    """Update an existing billable metric."""

    API_RESOURCE: ClassVar[str] = 'billable_metrics'
    RESPONSE_MODEL: ClassVar[Type[BillableMetricResponse]] = BillableMetricResponse
    ROOT_NAME: ClassVar[str] = 'billable_metric'


billable_metrics_operations_config: Mapping[str, Callable[..., Callable]] = {
    'create': CreateBillableMetric,
    'destroy': DestroyBillableMetric,
    'find': FindBillableMetric,
    'find_all': FindAllBillableMetrics,
    'update': UpdateBillableMetric,
}

groups_operations_config: Mapping[str, Callable[..., Callable]] = {
    'find_all': FindAllBillableMetricGroups,
}
