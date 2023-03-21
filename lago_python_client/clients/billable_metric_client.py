from typing import ClassVar, Type

from pydantic import BaseModel

from .base_client import BaseClient
from ..mixins import CreateCommandMixin, DestroyCommandMixin, FindAllCommandMixin, FindCommandMixin, UpdateCommandMixin
from ..models.billable_metric import BillableMetricResponse


class BillableMetricClient(CreateCommandMixin, DestroyCommandMixin, FindAllCommandMixin, FindCommandMixin, UpdateCommandMixin, BaseClient):
    API_RESOURCE: ClassVar[str] = 'billable_metrics'
    RESPONSE_MODEL: ClassVar[Type[BaseModel]] = BillableMetricResponse
    ROOT_NAME: ClassVar[str] = 'billable_metric'
