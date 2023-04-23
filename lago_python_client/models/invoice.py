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


class InvoiceMetadataList(BaseModel):
    __root__: List[InvoiceMetadata]


class Invoice(BaseModel):
    payment_status: Optional[str]
    metadata: Optional[InvoiceMetadataList]


class InvoiceResponse(BaseResponseModel):
    lago_id: str
    sequential_id: int
    number: str
    issuing_date: Optional[str]
    invoice_type: str
    status: str
    payment_status: str
    amount_cents: int
    amount_currency: str
    vat_amount_cents: int
    vat_amount_currency: str
    total_amount_cents: int
    total_amount_currency: str
    file_url: Optional[str]
    customer: Optional[CustomerResponse]
    subscriptions: Optional[SubscriptionsResponse]
    fees: Optional[FeesResponse]
    credits: Optional[CreditsResponse]
    metadata: Optional[InvoiceMetadataList]
