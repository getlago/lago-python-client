from typing import List, Optional, Dict

from lago_python_client.base_model import BaseModel

from ..base_model import BaseResponseModel


class RecurringTransactionRule(BaseModel):
    lago_id: Optional[str]
    interval: Optional[str]
    threshold_credits: Optional[str]
    trigger: Optional[str]
    method: Optional[str]
    paid_credits: Optional[str]
    granted_credits: Optional[str]
    started_at: Optional[str]
    expiration_at: Optional[str]
    target_ongoing_balance: Optional[str]
    transaction_metadata: Optional[List[Dict[str, str]]]
    transaction_name: Optional[str]
    ignore_paid_top_up_limits: Optional[bool]


class RecurringTransactionRuleResponse(BaseModel):
    lago_id: Optional[str]
    interval: Optional[str]
    threshold_credits: Optional[str]
    trigger: Optional[str]
    method: Optional[str]
    paid_credits: Optional[str]
    granted_credits: Optional[str]
    started_at: Optional[str]
    expiration_at: Optional[str]
    status: Optional[str]
    target_ongoing_balance: Optional[str]
    created_at: Optional[str]
    transaction_metadata: Optional[List[Dict[str, str]]]
    transaction_name: Optional[str]
    ignore_paid_top_up_limits: Optional[bool]


class RecurringTransactionRuleList(BaseModel):
    __root__: List[RecurringTransactionRule]


class RecurringTransactionRuleResponseList(BaseModel):
    __root__: List[RecurringTransactionRuleResponse]


class AppliesTo(BaseModel):
    fee_types: Optional[List[str]]
    billable_metric_codes: Optional[List[str]]


class Wallet(BaseModel):
    external_customer_id: Optional[str]
    rate_amount: Optional[str]
    name: Optional[str]
    paid_credits: Optional[str]
    granted_credits: Optional[str]
    expiration_at: Optional[str]
    currency: Optional[str]
    recurring_transaction_rules: Optional[RecurringTransactionRuleList]
    transaction_metadata: Optional[List[Dict[str, str]]]
    transaction_name: Optional[str]
    applies_to: Optional[AppliesTo]
    invoice_requires_successful_payment: Optional[bool]
    paid_top_up_max_amount_cents: Optional[int]
    paid_top_up_min_amount_cents: Optional[int]
    ignore_paid_top_up_limits_on_creation: Optional[bool]


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
    applies_to: Optional[AppliesTo]
    invoice_requires_successful_payment: Optional[bool]
    paid_top_up_max_amount_cents: Optional[int]
    paid_top_up_min_amount_cents: Optional[int]
