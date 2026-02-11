from typing import List, Optional

from ..base_model import BaseModel, BaseResponseModel


class AlertThresholdInput(BaseModel):
    code: Optional[str] = None
    value: str
    recurring: Optional[bool] = None


class AlertInput(BaseModel):
    alert_type: str
    code: str
    name: Optional[str] = None
    billable_metric_code: Optional[str] = None
    thresholds: List[AlertThresholdInput]


class BatchAlertInput(BaseModel):
    alerts: List[AlertInput]


class AlertThresholdResponse(BaseResponseModel):
    code: Optional[str]
    value: str
    recurring: bool


class AlertResponse(BaseResponseModel):
    lago_id: str
    lago_organization_id: str
    external_subscription_id: str
    alert_type: str
    code: str
    name: Optional[str]
    previous_value: Optional[str]
    last_processed_at: Optional[str]
    thresholds: Optional[List[AlertThresholdResponse]]
    created_at: Optional[str]
