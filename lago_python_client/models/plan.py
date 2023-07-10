from typing import Optional

from pydantic import BaseModel

from .charge import Charges, ChargesResponse
from .tax import Taxes, TaxesResponse
from ..base_model import BaseResponseModel


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


class PlanResponse(BaseResponseModel):
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
    taxes: Optional[TaxesResponse]
