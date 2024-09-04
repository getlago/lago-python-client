from typing import List, Optional

from lago_python_client.base_model import BaseModel

from ..base_model import BaseResponseModel
from .customer import CustomerResponse

class PaymentRequest(BaseModel):
    email: str
    external_customer_id: str
    lago_invoice_ids: List[str]


class PaymentRequestInvoiceResponse(BaseResponseModel):
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
    sub_total_excluding_taxes_amount_cents: int
    sub_total_including_taxes_amount_cents: int
    total_amount_cents: int
    prepaid_credit_amount_cents: int
    file_url: Optional[str]


class PaymentRequestInvoicesResponse(BaseResponseModel):
    __root__: List[PaymentRequestInvoiceResponse]


class PaymentRequestResponse(BaseResponseModel):
    lago_id: str
    email: str
    amount_cents: int
    amount_currency: str
    payment_status: str
    created_at: str
    customer: Optional[CustomerResponse]
    invoices: Optional[PaymentRequestInvoicesResponse]


class PaymentRequestsResponse(BaseResponseModel):
    __root__: List[PaymentRequestResponse]
