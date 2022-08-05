from pydantic import BaseModel, Field
from typing import Optional


class Subscription(BaseModel):
    plan_code: str
    customer_id: str
    billing_time: str


class SubscriptionResponse(BaseModel):
    lago_id: str
    lago_customer_id: Optional[str]
    customer_id: Optional[str]
    canceled_at: Optional[str]
    created_at: Optional[str]
    plan_code: Optional[str]
    started_at: Optional[str]
    status: Optional[str]
    billing_time: Optional[str]
    terminated_at: Optional[str]
