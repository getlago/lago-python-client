from typing import List, Optional

from lago_python_client.base_model import BaseModel
from .payment_method import PaymentMethod
from .plan import PlanOverrides
from ..base_model import BaseResponseModel


class Subscription(BaseModel):
    plan_code: Optional[str]
    external_customer_id: Optional[str]
    name: Optional[str]
    external_id: Optional[str]
    subscription_at: Optional[str]
    billing_time: Optional[str]
    ending_at: Optional[str]
    plan_overrides: Optional[PlanOverrides]
    payment_method: Optional[PaymentMethod]


class Subscriptions(BaseModel):
    external_ids: Optional[List[str]]
    plan_code: Optional[str]
    terminated_at: Optional[str]


class SubscriptionResponse(BaseResponseModel):
    lago_id: str
    lago_customer_id: Optional[str]
    external_customer_id: Optional[str]
    canceled_at: Optional[str]
    created_at: Optional[str]
    plan_code: Optional[str]
    plan_amount_cents: Optional[str]
    plan_amount_currency: Optional[str]
    started_at: Optional[str]
    status: Optional[str]
    name: Optional[str]
    external_id: Optional[str]
    billing_time: Optional[str]
    terminated_at: Optional[str]
    ending_at: Optional[str]
    trial_ended_at: Optional[str]
    subscription_date: Optional[str]
    subscription_at: Optional[str]
    previous_plan_code: Optional[str]
    next_plan_code: Optional[str]
    downgrade_plan_date: Optional[str]
    current_billing_period_started_at: Optional[str]
    current_billing_period_ending_at: Optional[str]
    on_termination_credit_note: Optional[str]
    on_termination_invoice: Optional[str]
    payment_method: Optional[PaymentMethod]


class SubscriptionsResponse(BaseResponseModel):
    __root__: List[SubscriptionResponse]
