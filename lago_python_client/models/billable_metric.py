from pydantic import BaseModel, Field
from typing import Optional, List, Union

class BillableMetricGroup(BaseModel):
    key: Optional[str]
    values: Optional[List[Union[str, dict]]]

class BillableMetric(BaseModel):
    name: Optional[str]
    code: Optional[str]
    description: Optional[str]
    aggregation_type: Optional[str]
    field_name: Optional[str]
    group: Optional[BillableMetricGroup]

class BillableMetricResponse(BaseModel):
    lago_id: str
    name: str
    code: str
    description: Optional[str]
    aggregation_type: Optional[str]
    field_name: Optional[str]
    created_at: str
    group: BillableMetricGroup
