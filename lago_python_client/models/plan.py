from pydantic import BaseModel, Field
from typing import Optional, List, Union

class Charge(BaseModel):
    id: Optional[str]
    billable_metric_id: Optional[str]
    amount_currency: Optional[str]
    charge_model: Optional[str]
    properties: Optional[Union[dict, list]]

class Charges(BaseModel):
    __root__: List[Charge]

class Plan(BaseModel):
    name: Optional[str]
    code: Optional[str]
    interval: Optional[str]
    description: Optional[str]
    amount_cents: Optional[int]
    amount_currency: Optional[str]
    trial_period: Optional[float]
    pay_in_advance: Optional[bool]
    bill_charges_monthly: Optional[bool]
    charges: Optional[Charges]


class PlanResponse(BaseModel):
    lago_id: str
    name: str
    created_at: str
    code: str
    interval: Optional[str]
    description: Optional[str]
    amount_cents: Optional[int]
    amount_currency: Optional[str]
    trial_period: Optional[float]
    pay_in_advance: Optional[bool]
    bill_charges_monthly: Optional[bool]
    charges: Optional[Charges]
