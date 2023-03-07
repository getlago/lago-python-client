from typing import ClassVar, Dict

from .base_client import BaseClient
from lago_python_client.models.billable_metric import BillableMetricResponse


class BillableMetricClient(BaseClient):
    API_RESOURCE: ClassVar[str] = 'billable_metrics'
    ROOT_NAME: ClassVar[str] = 'billable_metric'

    def prepare_response(self, data: Dict):
        return BillableMetricResponse.parse_obj(data)
