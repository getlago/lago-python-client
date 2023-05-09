from typing import List, Optional

from pydantic import BaseModel

from .credit import CreditsResponse
from .customer import CustomerResponse
from .fee import FeesResponse
from .subscription import SubscriptionsResponse
from ..base_model import BaseResponseModel


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


class InvoiceResponse(BaseResponseModel):
    lago_id: str
    sequential_id: int
    number: str
    issuing_date: Optional[str]
    invoice_type: str
    version_number: int
    status: str
    payment_status: str
    currency: str
    fees_amount_cents: int
    coupons_amount_cents: int
    vat_amount_cents: int
    credit_notes_amount_cents: int
    sub_total_vat_excluded_amount_cents: int
    sub_total_vat_included_amount_cents: int
    total_amount_cents: int
    prepaid_credit_amount_cents: int
    file_url: Optional[str]
    customer: Optional[CustomerResponse]
    subscriptions: Optional[SubscriptionsResponse]
    fees: Optional[FeesResponse]
    credits: Optional[CreditsResponse]
    metadata: Optional[InvoiceMetadataList]

    # NOTE(legacy): Deprecated fields that will be removed in the future
    legacy: bool
    amount_cents: int
    credit_amount_cents: int
    amount_currency: str
    vat_amount_currency: str
    credit_amount_currency: str
    total_amount_currency: str
