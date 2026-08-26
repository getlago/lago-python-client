from typing import List, Optional

from lago_python_client.base_model import BaseModel

from ..base_model import BaseResponseModel
from .quote import QuoteBillingItemsResponse


class OrderExecute(BaseModel):
    execution_mode: Optional[str]


class OrderExecutionRecordResponse(BaseResponseModel):
    executed_at: Optional[str]
    execution_mode: Optional[str]
    invoice_id: Optional[str]
    subscription_ids: Optional[List[str]]
    terminated_subscription_ids: Optional[List[str]]
    applied_coupon_ids: Optional[List[str]]
    wallet_ids: Optional[List[str]]
    errors: Optional[List[str]]


class OrderResponse(BaseResponseModel):
    lago_id: str
    number: str
    status: str
    order_type: str
    execution_mode: Optional[str]
    currency: Optional[str]
    executed_at: Optional[str]
    execution_record: Optional[OrderExecutionRecordResponse]
    lago_organization_id: str
    lago_customer_id: str
    lago_order_form_id: str
    created_at: str
    updated_at: str
    # Omitted from the webhook payloads, being a heavy blob.
    billing_snapshot: Optional[QuoteBillingItemsResponse]
