from typing import Optional

from pydantic import BaseModel

from ..base_model import BaseResponseModel


class Wallet(BaseModel):
    external_customer_id: Optional[str]
    rate_amount: Optional[str]
    name: Optional[str]
    paid_credits: Optional[str]
    granted_credits: Optional[str]
    expiration_at: Optional[str]
    currency: Optional[str]


class WalletResponse(BaseResponseModel):
    lago_id: str
    lago_customer_id: str
    external_customer_id: str
    status: str
    currency: str
    name: Optional[str]
    rate_amount: str
    credits_balance: str
    balance: str
    consumed_credits: str
    created_at: str
    expiration_at: Optional[str]
    last_balance_sync_at: Optional[str]
    last_consumed_credit_at: Optional[str]
    terminated_at: Optional[str]
