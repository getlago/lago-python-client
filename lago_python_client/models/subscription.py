from typing import List, Optional

from pydantic import BaseModel
from .plan import PlanOverrides
from ..base_model import BaseResponseModel


class Subscription(BaseModel):
    plan_code: Optional[str]
    external_customer_id: Optional[str]
    name: Optional[str]
    external_id: Optional[str]
    subscription_date: Optional[str]
    billing_time: Optional[str]
    ending_at: Optional[str]
    plan_overrides: Optional[PlanOverrides]


class SubscriptionResponse(BaseResponseModel):
    lago_id: str
    lago_customer_id: Optional[str]
    external_customer_id: Optional[str]
    canceled_at: Optional[str]
    created_at: Optional[str]
    plan_code: Optional[str]
    started_at: Optional[str]
    status: Optional[str]
    name: Optional[str]
    external_id: Optional[str]
    billing_time: Optional[str]
    terminated_at: Optional[str]
    ending_at: Optional[str]
    subscription_date: Optional[str]
    previous_plan_code: Optional[str]
    next_plan_code: Optional[str]
    downgrade_plan_date: Optional[str]


class SubscriptionsResponse(BaseResponseModel):
    __root__: List[SubscriptionResponse]
