from typing import Any, Dict, List, Optional, Union

from lago_python_client.base_model import BaseModel

from ..base_model import BaseResponseModel


class BillableMetricGroup(BaseModel):
    key: Optional[str]
    values: Optional[List[Union[str, Dict[str, Any]]]]


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
    field_name: Optional[str]
    group: Optional[BillableMetricGroup]
    filters: Optional[BillableMetricFilters]


class BillableMetricResponse(BaseResponseModel):
    lago_id: str
    name: str
    code: str
    description: Optional[str]
    recurring: Optional[bool]
    aggregation_type: Optional[str]
    weighted_interval: Optional[str]
    field_name: Optional[str]
    created_at: str
    group: BillableMetricGroup
    filters: BillableMetricFilters
    active_subscriptions_count: int
    draft_invoices_count: int
    plans_count: int
