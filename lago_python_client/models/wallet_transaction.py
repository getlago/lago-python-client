from typing import Dict, List, Optional

from lago_python_client.base_model import BaseModel

from ..base_model import BaseResponseModel
from .invoice_custom_section import AppliedInvoiceCustomSections, InvoiceCustomSectionInput
from .payment_method import PaymentMethod


class WalletTransaction(BaseModel):
    wallet_id: Optional[str]
    paid_credits: Optional[str]
    granted_credits: Optional[str]
    voided_credits: Optional[str]
    invoice_requires_successful_payment: Optional[bool]
    metadata: Optional[List[Dict[str, str]]]
    name: Optional[str]
    ignore_paid_top_up_limits: Optional[bool]
    payment_method: Optional[PaymentMethod]
    invoice_custom_section: Optional[InvoiceCustomSectionInput]


class WalletTransactionResponse(BaseResponseModel):
    lago_id: str
    lago_wallet_id: str
    lago_invoice_id: Optional[str]
    lago_voided_invoice_id: Optional[str]
    status: str
    source: str
    transaction_status: str
    transaction_type: str
    amount: str
    credit_amount: str
    remaining_amount_cents: Optional[int]
    remaining_credit_amount: Optional[str]
    settled_at: Optional[str]
    failed_at: Optional[str]
    created_at: str
    metadata: Optional[List[Dict[str, str]]]
    name: Optional[str]
    invoice_requires_successful_payment: Optional[bool]
    payment_method: Optional[PaymentMethod]
    applied_invoice_custom_sections: Optional[AppliedInvoiceCustomSections]


class WalletTransactionConsumptionResponse(BaseResponseModel):
    lago_id: str
    amount_cents: int
    credit_amount: str
    created_at: str
    wallet_transaction: Optional[WalletTransactionResponse]


class WalletTransactionFundingResponse(BaseResponseModel):
    lago_id: str
    amount_cents: int
    credit_amount: str
    created_at: str
    wallet_transaction: Optional[WalletTransactionResponse]
