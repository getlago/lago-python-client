from typing import List, Literal, Optional, TypedDict, Union

from ..base_model import BaseModel, BaseResponseModel

PaymentStatusFilter = Literal["pending", "processing", "succeeded", "failed"]
PaymentProviderFilter = Literal["stripe", "gocardless", "cashfree", "adyen", "flutterwave", "moneyhash"]
PaymentMethodFilter = Literal[
    "card", "sepa_debit", "us_bank_account", "bacs_debit", "link", "boleto", "crypto", "customer_balance"
]
PaymentTypeFilter = Literal["manual", "provider"]
PayableTypeFilter = Literal["Invoice", "PaymentRequest"]


class PaymentFilters(TypedDict, total=False):
    """Optional list filters; amounts are inclusive integer cents and dates are ISO-8601 dates."""

    page: int
    per_page: int
    external_customer_id: str
    invoice_id: str
    payment_status: Union[PaymentStatusFilter, List[PaymentStatusFilter]]
    payment_statuses: Union[PaymentStatusFilter, List[PaymentStatusFilter]]
    amount_from: int
    amount_to: int
    receipt_number: str
    created_at_from: str
    created_at_to: str
    payment_provider_type: Union[PaymentProviderFilter, List[PaymentProviderFilter]]
    payment_method_type: Union[PaymentMethodFilter, List[PaymentMethodFilter]]
    currency: str
    invoice_number: str
    payment_type: Union[PaymentTypeFilter, List[PaymentTypeFilter]]
    payable_type: Union[PayableTypeFilter, List[PayableTypeFilter]]
    search_term: str


class Payment(BaseModel):
    invoice_id: str
    amount_cents: int
    reference: str
    paid_at: Optional[str]


class PaymentResponse(BaseResponseModel):
    lago_id: str
    invoice_ids: List[str]
    invoice_numbers: List[str]
    amount_cents: int
    amount_currency: str
    payment_status: str
    type: str
    reference: Optional[str]
    external_payment_id: Optional[str]
    created_at: str


class PaymentsResponse(BaseResponseModel):
    __root__: List[PaymentResponse]
