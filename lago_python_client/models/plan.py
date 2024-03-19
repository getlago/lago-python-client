from typing import List, Optional

from lago_python_client.base_model import BaseModel

from .charge import Charges, ChargesResponse, ChargesOverrides
from .minimum_commitment import MinimumCommitment, MinimumCommitmentResponse, MinimumCommitmentOverrides
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
    minimum_commitment: Optional[MinimumCommitment]
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
    minimum_commitment: Optional[MinimumCommitmentResponse]
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
    minimum_commitment: Optional[MinimumCommitmentOverrides]
    tax_codes: Optional[List[str]]
