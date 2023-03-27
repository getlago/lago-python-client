from typing import Optional

from pydantic import BaseModel

from ..base_model import BaseResponseModel


class WalletTransaction(BaseModel):
    wallet_id: Optional[str]
    paid_credits: Optional[str]
    granted_credits: Optional[str]


class WalletTransactionResponse(BaseResponseModel):
    lago_id: str
    lago_wallet_id: str
    status: str
    transaction_type: str
    amount: str
    credit_amount: str
    settled_at: Optional[str]
    created_at: str
