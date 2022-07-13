from typing import List
from pydantic import BaseModel, Field


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


class CustomerUsageResponse(BaseModel):
  from_date: str
  to_date: str
  issuing_date: str
  amount_cents: int
  amount_currency: str
  total_amount_cents: int
  total_amount_currency: str
  vat_amount_cents: int
  vat_amount_currency: str
  charges_usage: List[ChargeUsage]
