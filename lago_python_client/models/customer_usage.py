from typing import List

from pydantic import BaseModel

from ..base_model import BaseResponseModel


class Metric(BaseModel):
    lago_id: str
    name: str
    code: str
    aggregation_type: str


class ChargeObject(BaseModel):
    lago_id: str
    charge_model: str


class ChargeUsage(BaseModel):
    units: float
    amount_cents: int
    amount_currency: str
    charge: ChargeObject
    billable_metric: Metric


class CustomerUsageResponse(BaseResponseModel):
    from_datetime: str
    to_datetime: str
    issuing_date: str
    currency: str
    amount_cents: int
    total_amount_cents: int
    taxes_amount_cents: int
    charges_usage: List[ChargeUsage]
