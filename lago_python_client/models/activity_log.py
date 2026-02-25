from typing import Optional

from lago_python_client.base_model import BaseModel

from ..base_model import BaseResponseModel


class ActivityLog(BaseModel):
    activity_type: str
    activity_object: Optional[dict]
    activity_object_changes: Optional[dict]
    activity_source: str
    logged_at: str
    resource_type: str
    created_at: str
    activity_id: str
    external_customer_id: Optional[str]
    external_subscription_id: Optional[str]
    resource_id: str
    user_email: Optional[str]


class ActivityLogResponse(BaseResponseModel):
    activity_id: str
    activity_type: str
    activity_source: str
    activity_object: Optional[dict]
    activity_object_changes: Optional[dict]
    user_email: Optional[str]
    resource_id: str
    resource_type: str
    external_customer_id: Optional[str]
    external_subscription_id: Optional[str]
    logged_at: str
    created_at: str
