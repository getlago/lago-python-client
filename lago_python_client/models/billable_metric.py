from pydantic import BaseModel, Field
from typing import Optional


class BillableMetric(BaseModel):
    name: str
    code: str
    description: Optional[str]
    aggregation_type: Optional[str]
    field_name: Optional[str]


class BillableMetricResponse(BaseModel):
    lago_id: str
    name: str
    code: str
    description: str
    aggregation_type: str
    field_name: str
    created_at: str
