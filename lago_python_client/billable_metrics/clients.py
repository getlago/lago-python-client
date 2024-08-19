import sys
from typing import Any, ClassVar, Type, Union

from ..base_client import BaseClient
from ..mixins import CreateCommandMixin, DestroyCommandMixin, FindAllCommandMixin, FindCommandMixin, UpdateCommandMixin
from ..models.billable_metric import BillableMetricResponse
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
