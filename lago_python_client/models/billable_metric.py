from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel

from ..base_model import BaseResponseModel


class BillableMetricGroup(BaseModel):
    key: Optional[str]
    values: Optional[List[Union[str, Dict[str, Any]]]]


class BillableMetric(BaseModel):
    name: Optional[str]
    code: Optional[str]
    description: Optional[str]
    recurring: Optional[bool]
    aggregation_type: Optional[str]
    weighted_interval: Optional[str]
    field_name: Optional[str]
    group: Optional[BillableMetricGroup]


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
    active_subscriptions_count: int
    draft_invoices_count: int
    plans_count: int
