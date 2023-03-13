from pydantic import BaseModel, Field
from typing import Optional, List

class GroupProperties(BaseModel):
    group_id: Optional[str]
    values: Optional[dict]


class Charge(BaseModel):
    id: Optional[str]
    billable_metric_id: Optional[str]
    charge_model: Optional[str]
    properties: Optional[dict]
    group_properties: Optional[GroupProperties]

class Charges(BaseModel):
    __root__: List[Charge]

class ChargeResponse(BaseModel):
    lago_id: Optional[str]
    lago_billable_metric_id: Optional[str]
    billable_metric_code: Optional[str]
    charge_model: Optional[str]
    properties: Optional[dict]
    group_properties: Optional[GroupProperties]

class ChargesResponse(BaseModel):
    __root__: List[ChargeResponse]
