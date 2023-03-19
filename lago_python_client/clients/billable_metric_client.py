from typing import ClassVar, Type

from .base_client import BaseClient
from ..mixins import CreateCommandMixin, DestroyCommandMixin, FindAllCommandMixin, FindCommandMixin, UpdateCommandMixin
from ..models.billable_metric import BillableMetricResponse


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
