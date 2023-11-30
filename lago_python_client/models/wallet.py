from typing import List, Optional

from pydantic import BaseModel

from ..base_model import BaseResponseModel


class RecurringTransactionRule(BaseModel):
    lago_id: Optional[str]
    rule_type: Optional[str]
    interval: Optional[str]
    threshold_credits: Optional[str]
    paid_credits: Optional[str]
    granted_credits: Optional[str]


class RecurringTransactionRuleResponse(BaseModel):
    lago_id: Optional[str]
    rule_type: Optional[str]
    interval: Optional[str]
    threshold_credits: Optional[str]
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
    balance: str # NOTE(legacy)
