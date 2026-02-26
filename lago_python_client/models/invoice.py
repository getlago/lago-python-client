from typing import List, Optional

from lago_python_client.base_model import BaseModel

from ..base_model import BaseResponseModel
from .billing_period import BillingPeriodsResponse
from .coupon import CouponsList
from .credit import CreditsResponse
from .customer import Customer, CustomerResponse
from .error_detail import ErrorDetailsResponse
from .fee import FeesResponse
from .payment_method import PaymentMethod
from .subscription import Subscriptions, SubscriptionsResponse
from .usage_threshold import UsageThreshold


# Deprecated: Will be removed in the future
class InvoicePaymentStatusChange(BaseModel):
    payment_status: str


class InvoiceMetadata(BaseModel):
    id: Optional[str]
    key: Optional[str]
    value: Optional[str]


class InvoiceFee(BaseModel):
    add_on_code: Optional[str]
    unit_amount_cents: Optional[int]
    units: Optional[float]
    description: Optional[str]
    from_datetime: Optional[str]
    to_datetime: Optional[str]
    invoice_display_name: Optional[str]
    tax_codes: Optional[List[str]]


class InvoiceMetadataList(BaseModel):
    __root__: List[InvoiceMetadata]


class InvoiceFeesList(BaseModel):
    __root__: List[InvoiceFee]


class Invoice(BaseModel):
    payment_status: Optional[str]
    metadata: Optional[InvoiceMetadataList]


class OneOffInvoice(BaseModel):
    external_customer_id: Optional[str]
    currency: Optional[str]
    fees: Optional[InvoiceFeesList]
    error_details: Optional[ErrorDetailsResponse]
    payment_method: Optional[PaymentMethod]


class InvoicePreview(BaseModel):
    plan_code: Optional[str]
    billing_time: Optional[str]
    subscription_at: Optional[str]
    coupons: Optional[CouponsList]
    customer: Optional[Customer]
    subscriptions: Optional[Subscriptions]


class InvoiceAppliedTax(BaseResponseModel):
    lago_id: Optional[str]
    lago_invoice_id: Optional[str]
    lago_tax_id: Optional[str]
    tax_name: Optional[str]
    tax_code: Optional[str]
    tax_rate: Optional[float]
    tax_description: Optional[str]
    amount_cents: Optional[int]
    amount_currency: Optional[str]
    fees_amount_cents: Optional[int]
    created_at: Optional[str]


class InvoiceAppliedTaxes(BaseResponseModel):
    __root__: List[InvoiceAppliedTax]


class InvoiceAppliedInvoiceCustomSection(BaseResponseModel):
    lago_id: Optional[str]
    lago_invoice_id: Optional[str]
    code: Optional[str]
    details: Optional[str]
    display_name: Optional[str]
    created_at: Optional[str]


class InvoiceAppliedInvoiceCustomSections(BaseResponseModel):
    __root__: List[InvoiceAppliedInvoiceCustomSection]


class InvoiceAppliedUsageThreshold(BaseResponseModel):
    lifetime_usage_amount_cents: Optional[int]
    created_at: Optional[str]
    usage_threshold: Optional[UsageThreshold]


class InvoiceAppliedUsageThresholds(BaseResponseModel):
    __root__: List[InvoiceAppliedUsageThreshold]


class InvoiceResponse(BaseResponseModel):
    lago_id: str
    sequential_id: Optional[int]
    number: str
    issuing_date: Optional[str]
    payment_dispute_lost_at: Optional[str]
    payment_due_date: Optional[str]
    payment_overdue: bool
    net_payment_term: int
    invoice_type: str
    version_number: int
    status: str
    payment_status: str
    currency: str
    fees_amount_cents: int
    coupons_amount_cents: int
    taxes_amount_cents: int
    credit_notes_amount_cents: int
    progressive_billing_credit_amount_cents: int
    sub_total_excluding_taxes_amount_cents: int
    sub_total_including_taxes_amount_cents: int
    total_amount_cents: int
    total_due_amount_cents: int
    prepaid_credit_amount_cents: int

    file_url: Optional[str]
    customer: Optional[CustomerResponse]
    billing_periods: Optional[BillingPeriodsResponse]
    subscriptions: Optional[SubscriptionsResponse]
    fees: Optional[FeesResponse]
    credits: Optional[CreditsResponse]
    metadata: Optional[InvoiceMetadataList]
    applied_taxes: Optional[InvoiceAppliedTaxes]
    applied_invoice_custom_sections: Optional[InvoiceAppliedInvoiceCustomSections]
    applied_usage_thresholds: Optional[InvoiceAppliedUsageThresholds]
    error_details: Optional[ErrorDetailsResponse]
    billing_entity_code: Optional[str]
