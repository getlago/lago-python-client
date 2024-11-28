from typing import Any, Dict, List, Optional, Union

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
    rounding_function: Optional[str]
    rounding_precision: Optional[int]
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
    rounding_function: Optional[str]
    rounding_precision: Optional[int]
    aggregation_type: Optional[str]
    weighted_interval: Optional[str]
    expression: Optional[str]
    field_name: Optional[str]
    created_at: str
    filters: BillableMetricFilters


class BillableMetricEvaluateExpressionEvent(BaseModel):
    code: Optional[str]
    timestamp: Optional[Union[str, int]]
    properties: Optional[Dict[str, Any]]


class BillableMetricEvaluateExpression(BaseModel):
    expression: str
    event: BillableMetricEvaluateExpressionEvent


class BillableMetricEvaluateExpressionResponse(BaseResponseModel):
    value: Union[str, int, float]
