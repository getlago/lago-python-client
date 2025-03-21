from typing import Optional, List, Dict

from lago_python_client.base_model import BaseModel

from ..base_model import BaseResponseModel


class WalletTransaction(BaseModel):
    wallet_id: Optional[str]
    paid_credits: Optional[str]
    granted_credits: Optional[str]
    voided_credits: Optional[str]
    metadata: Optional[List[Dict[str, str]]]


class WalletTransactionResponse(BaseResponseModel):
    lago_id: str
    lago_wallet_id: str
    status: str
    source: str
    transaction_status: str
    transaction_type: str
    amount: str
    credit_amount: str
    settled_at: Optional[str]
    failed_at: Optional[str]
    created_at: str
    metadata: Optional[List[Dict[str, str]]]
