from typing import List, Optional

from lago_python_client.base_model import BaseModel

from ..base_model import BaseResponseModel


class RecurringTransactionRule(BaseModel):
    lago_id: Optional[str]
    interval: Optional[str]
    threshold_credits: Optional[str]
    trigger: Optional[str]
    paid_credits: Optional[str]
    granted_credits: Optional[str]


class RecurringTransactionRuleResponse(BaseModel):
    lago_id: Optional[str]
    interval: Optional[str]
    threshold_credits: Optional[str]
    trigger: Optional[str]
    paid_credits: Optional[str]
    granted_credits: Optional[str]
    created_at: Optional[str]


class RecurringTransactionRuleList(BaseModel):
    __root__: List[RecurringTransactionRule]


class RecurringTransactionRuleResponseList(BaseModel):
    __root__: List[RecurringTransactionRuleResponse]


class Wallet(BaseModel):
    external_customer_id: Optional[str]
    rate_amount: Optional[str]
    name: Optional[str]
    paid_credits: Optional[str]
    granted_credits: Optional[str]
    expiration_at: Optional[str]
    currency: Optional[str]
    recurring_transaction_rules: Optional[RecurringTransactionRuleList]


class WalletResponse(BaseResponseModel):
    lago_id: str
    lago_customer_id: str
    external_customer_id: str
    status: str
    currency: str
    name: Optional[str]
    rate_amount: str
    credits_balance: str
    balance_cents: int
    consumed_credits: str
    created_at: str
    expiration_at: Optional[str]
    last_balance_sync_at: Optional[str]
    last_consumed_credit_at: Optional[str]
    terminated_at: Optional[str]
    recurring_transaction_rules: Optional[RecurringTransactionRuleResponseList]
    ongoing_balance_cents: int
    ongoing_usage_balance_cents: int
    credits_ongoing_balance: str
    credits_ongoing_usage_balance: str
    balance: str # NOTE(legacy)
