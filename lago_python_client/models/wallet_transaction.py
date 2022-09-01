from pydantic import BaseModel, Field
from typing import Optional


class WalletTransaction(BaseModel):
    wallet_id: Optional[str]
    paid_credits: Optional[float]
    granted_credits: Optional[float]


class WalletTransactionResponse(BaseModel):
    lago_id: str
    lago_wallet_id: str
    status: str
    transaction_type: str
    amount: float
    credit_amount: float
    settled_at: Optional[str]
    created_at: str
