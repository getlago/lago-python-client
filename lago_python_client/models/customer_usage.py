from typing import List, Optional

from pydantic import BaseModel

from ..base_model import BaseResponseModel


class Metric(BaseModel):
    lago_id: str
    name: str
    code: str
    aggregation_type: str

class Group(BaseModel):
    lago_id: str
    key: Optional[str]
    value: str
    units: str
    amount_cents: int

class ChargeObject(BaseModel):
    lago_id: str
    charge_model: str
    invoice_display_name: Optional[str]


class ChargeUsage(BaseModel):
    units: float
    events_count: int
    amount_cents: int
    amount_currency: str
    charge: ChargeObject
    billable_metric: Metric
    groups: List[Group]


class CustomerUsageResponse(BaseResponseModel):
    from_datetime: str
    to_datetime: str
    issuing_date: str
    invoice_id: Optional[str]
    currency: str
    amount_cents: int
    total_amount_cents: int
    taxes_amount_cents: int
    charges_usage: List[ChargeUsage]
