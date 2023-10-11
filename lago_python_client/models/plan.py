from typing import List, Optional

from pydantic import BaseModel

from .charge import Charges, ChargesResponse, ChargesOverrides
from .tax import Taxes, TaxesResponse
from ..base_model import BaseResponseModel


class Plan(BaseModel):
    name: Optional[str]
    invoice_display_name: Optional[str]
    code: Optional[str]
    interval: Optional[str]
    description: Optional[str]
    amount_cents: Optional[int]
    amount_currency: Optional[str]
    trial_period: Optional[float]
    pay_in_advance: Optional[bool]
    bill_charges_monthly: Optional[bool]
    charges: Optional[Charges]
    tax_codes: Optional[List[str]]


class PlanResponse(BaseResponseModel):
    lago_id: str
    name: str
    invoice_display_name: Optional[str]
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

class PlanOverrides(BaseModel):
    name: Optional[str]
    invoice_display_name: Optional[str]
    description: Optional[str]
    amount_cents: Optional[int]
    amount_currency: Optional[str]
    trial_period: Optional[float]
    charges: Optional[ChargesOverrides]
    tax_codes: Optional[List[str]]