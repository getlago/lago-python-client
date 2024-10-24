from typing import List, Optional

from lago_python_client.base_model import BaseModel

from ..base_model import BaseResponseModel


class BillableMetricFilter(BaseModel):
    key: Optional[str]
    values: Optional[List[str]]


class BillableMetricFilters(BaseModel):
    __root__: List[BillableMetricFilter]


class BillableMetric(BaseModel):
    name: Optional[str]
    code: Optional[str]
    description: Optional[str]
    recurring: Optional[bool]
    aggregation_type: Optional[str]
    weighted_interval: Optional[str]
    expression: Optional[str]
    field_name: Optional[str]
    filters: Optional[BillableMetricFilters]


class BillableMetricResponse(BaseResponseModel):
    lago_id: str
    name: str
    code: str
    description: Optional[str]
    recurring: Optional[bool]
    aggregation_type: Optional[str]
    weighted_interval: Optional[str]
    expression: Optional[str]
    field_name: Optional[str]
    created_at: str
    filters: BillableMetricFilters
    active_subscriptions_count: int
    draft_invoices_count: int
    plans_count: int
