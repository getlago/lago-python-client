from pydantic import BaseModel, Field
from typing import Optional, List
from .customer import CustomerResponse
from .subscription import SubscriptionsResponse

class InvoiceStatusChange(BaseModel):
    status: str

class InvoiceItemResponse(BaseModel):
    type: Optional[str]
    code: Optional[str]
    name: Optional[str]

class FeeResponse(BaseModel):
    lago_id: Optional[str]
    item: Optional[InvoiceItemResponse]
    amount_cents: Optional[int]
    amount_currency: Optional[str]
    vat_amount_cents: Optional[int]
    vat_amount_currency: Optional[str]
    units: Optional[float]
    events_count: Optional[int]

class FeesResponse(BaseModel):
    __root__: List[FeeResponse]

class CreditResponse(BaseModel):
    amount_cents: Optional[int]
    amount_currency: Optional[str]
    item: Optional[InvoiceItemResponse]

class CreditsResponse(BaseModel):
    __root__: List[CreditResponse]

class InvoiceResponse(BaseModel):
    lago_id: str
    sequential_id: int
    issuing_date: Optional[str]
    invoice_type: str
    status: str
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
