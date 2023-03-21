from typing import Optional

from pydantic import BaseModel


class WalletTransaction(BaseModel):
    wallet_id: Optional[str]
    paid_credits: Optional[str]
    granted_credits: Optional[str]


class WalletTransactionResponse(BaseModel):
    lago_id: str
    lago_wallet_id: str
    status: str
    transaction_type: str
    amount: str
    credit_amount: str
    settled_at: Optional[str]
    created_at: str
