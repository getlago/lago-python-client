from typing import Any, Dict, List, Optional

from pydantic import BaseModel

from ..base_model import BaseResponseModel


class GroupProperties(BaseModel):
    group_id: Optional[str]
    values: Optional[Dict[str, Any]]


class Charge(BaseModel):
    id: Optional[str]
    billable_metric_id: Optional[str]
    charge_model: Optional[str]
    pay_in_advance: Optional[bool]
    min_amount_cents: Optional[int]
    properties: Optional[Dict[str, Any]]
    group_properties: Optional[GroupProperties]


class Charges(BaseModel):
    __root__: List[Charge]


class ChargeResponse(BaseResponseModel):
    lago_id: Optional[str]
    lago_billable_metric_id: Optional[str]
    billable_metric_code: Optional[str]
    charge_model: Optional[str]
    pay_in_advance: Optional[bool]
    min_amount_cents: Optional[int]
    properties: Optional[Dict[str, Any]]
    group_properties: Optional[GroupProperties]


class ChargesResponse(BaseResponseModel):
    __root__: List[ChargeResponse]
