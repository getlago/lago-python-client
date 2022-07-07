from pydantic import BaseModel, Field
from typing import Optional


class BillableMetric(BaseModel):
    name: Optional[str]
    code: Optional[str]
    description: Optional[str]
    aggregation_type: Optional[str]
    field_name: Optional[str]


class BillableMetricResponse(BaseModel):
    lago_id: str
    name: str
    code: str
    description: Optional[str]
    aggregation_type: Optional[str]
    field_name: Optional[str]
    created_at: str
