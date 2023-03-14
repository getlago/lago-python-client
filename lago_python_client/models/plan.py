from pydantic import BaseModel, Field
from typing import Optional, List, Union

from .charge import Charges, ChargesResponse


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
    charges: Optional[ChargesResponse]
    active_subscriptions_count: int
    draft_invoices_count: int
