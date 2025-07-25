from typing import Any, Dict, List, Optional

from .invoice_item import InvoiceItemResponse
from ..base_model import BaseModel, BaseResponseModel


class Fee(BaseModel):
    payment_status: Optional[str]
    invoice_display_name: Optional[str]


class FeeAppliedTax(BaseResponseModel):
    lago_id: Optional[str]
    lago_fee_id: Optional[str]
    lago_tax_id: Optional[str]
    tax_name: Optional[str]
    tax_code: Optional[str]
    tax_rate: Optional[float]
    tax_description: Optional[str]
    amount_cents: Optional[int]
    amount_currency: Optional[str]
    created_at: Optional[str]


class FeeAppliedTaxes(BaseResponseModel):
    __root__: List[FeeAppliedTax]


class PricingUnitDetails(BaseResponseModel):
    lago_pricing_unit_id: Optional[str]
    pricing_unit_code: Optional[str]
    short_name: Optional[str]
    amount_cents: Optional[int]
    precise_amount_cents: Optional[str]
    unit_amount_cents: Optional[int]
    precise_unit_amount: Optional[str]
    conversion_rate: Optional[float]


class FeeResponse(BaseResponseModel):
    lago_id: Optional[str]
    lago_charge_id: Optional[str]
    lago_charge_filter_id: Optional[str]
    lago_invoice_id: Optional[str]
    lago_true_up_fee_id: Optional[str]
    lago_true_up_parent_fee_id: Optional[str]
    external_subscription_id: Optional[str]
    amount_cents: Optional[int]
    amount_currency: Optional[str]
    taxes_amount_cents: Optional[int]
    taxes_rate: Optional[float]
    total_amount_cents: Optional[int]
    unit_amount_cents: Optional[int]  # deprecated
    precise_unit_amount: Optional[str]
    precise_amount: Optional[str]
    precise_total_amount: Optional[str]
    taxes_precise_amount: Optional[str]
    total_amount_currency: Optional[str]
    units: Optional[float]
    events_count: Optional[int]
    payment_status: Optional[str]
    created_at: Optional[str]
    description: Optional[str]
    pay_in_advance: Optional[bool]
    invoiceable: Optional[bool]
    invoice_display_name: Optional[str]
    succeeded_at: Optional[str]
    failed_at: Optional[str]
    refunded_at: Optional[str]
    from_date: Optional[str]
    to_date: Optional[str]
    amount_details: Optional[Dict[str, Any]]
    pricing_unit_details: Optional[PricingUnitDetails]
    billing_entity_code: Optional[str]

    item: Optional[InvoiceItemResponse]
    applied_taxes: Optional[FeeAppliedTaxes]


class FeesResponse(BaseResponseModel):
    __root__: List[FeeResponse]
