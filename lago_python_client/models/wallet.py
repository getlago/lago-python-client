from pydantic import BaseModel, Field
from typing import Optional


class Wallet(BaseModel):
    external_customer_id: Optional[str]
    rate_amount: Optional[float]
    name: Optional[str]
    paid_credits: Optional[float]
    granted_credits: Optional[float]
    expiration_date: Optional[str]


class WalletResponse(BaseModel):
    lago_id: str
    lago_customer_id: str
    external_customer_id: str
    status: str
    currency: str
    name: Optional[str]
    rate_amount: float
    credits_balance: float
    balance: float
    consumed_credits: float
    created_at: str
    expiration_date: Optional[str]
    last_balance_sync_at: Optional[str]
    last_consumed_credit_at: Optional[str]
    terminated_at: Optional[str]
