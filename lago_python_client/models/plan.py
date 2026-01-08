from typing import Any, Dict, List, Optional

from lago_python_client.base_model import BaseModel

from .charge import Charges, ChargesResponse, ChargesOverrides
from .fixed_charge import (
    FixedCharges,
    FixedChargesResponse,
    FixedChargesOverrides,
)
from .usage_threshold import (
    UsageThresholds,
    UsageThresholdsResponse,
    UsageThresholdsOverrides,
)
from .minimum_commitment import (
    MinimumCommitment,
    MinimumCommitmentResponse,
    MinimumCommitmentOverrides,
)
from .tax import TaxesResponse
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
    bill_fixed_charges_monthly: Optional[bool]
    charges: Optional[Charges]
    fixed_charges: Optional[FixedCharges]
    minimum_commitment: Optional[MinimumCommitment]
    usage_thresholds: Optional[UsageThresholds]
    tax_codes: Optional[List[str]]
    cascade_updates: Optional[bool]
    metadata: Optional[Dict[str, Any]]


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
    bill_fixed_charges_monthly: Optional[bool]
    charges: Optional[ChargesResponse]
    fixed_charges: Optional[FixedChargesResponse]
    minimum_commitment: Optional[MinimumCommitmentResponse]
    usage_thresholds: Optional[UsageThresholdsResponse]
    taxes: Optional[TaxesResponse]
    metadata: Optional[Dict[str, Any]]


class PlanOverrides(BaseModel):
    name: Optional[str]
    invoice_display_name: Optional[str]
    description: Optional[str]
    amount_cents: Optional[int]
    amount_currency: Optional[str]
    trial_period: Optional[float]
    charges: Optional[ChargesOverrides]
    fixed_charges: Optional[FixedChargesOverrides]
    minimum_commitment: Optional[MinimumCommitmentOverrides]
    usage_thresholds: Optional[UsageThresholdsOverrides]
    tax_codes: Optional[List[str]]
    metadata: Optional[Dict[str, Any]]
