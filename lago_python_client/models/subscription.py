from pydantic import BaseModel, Field
from typing import Optional


class Subscription(BaseModel):
    plan_code: Optional[str]
    customer_id: Optional[str]
    name: Optional[str]
    subscription_id: Optional[str]
    unique_id: Optional[str]
    billing_time: Optional[str]


class SubscriptionResponse(BaseModel):
    lago_id: str
    lago_customer_id: Optional[str]
    customer_id: Optional[str]
    canceled_at: Optional[str]
    created_at: Optional[str]
    plan_code: Optional[str]
    started_at: Optional[str]
    status: Optional[str]
    name: Optional[str]
    unique_id: Optional[str]
    billing_time: Optional[str]
    terminated_at: Optional[str]
    subscription_date: Optional[str]
