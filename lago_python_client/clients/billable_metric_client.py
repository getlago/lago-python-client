from .base_client import BaseClient
from lago_python_client.models.billable_metric import BillableMetricResponse
from typing import Dict


class BillableMetricClient(BaseClient):
    def api_resource(self):
        return 'billable_metrics'

    def root_name(self):
        return 'billable_metric'

    def prepare_response(self, data: Dict):
        return BillableMetricResponse.parse_obj(data)
