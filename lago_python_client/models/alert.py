from typing import List, Optional

from ..base_model import BaseModel, BaseResponseModel
from .billable_metric import BillableMetricResponse


class AlertThreshold(BaseModel):
    code: str
    value: str
    recurring: bool


class AlertThresholdList(BaseModel):
    __root__: List[AlertThreshold]


class Alert(BaseModel):
    alert_type: str
    code: str
    name: Optional[str]
    thresholds: AlertThresholdList
    billable_metric_code: Optional[str]


class AlertThresholdResponse(BaseResponseModel):
    code: str
    value: str
    recurring: bool


class AlertThresholdResponseList(BaseResponseModel):
    __root__: List[AlertThresholdResponse]


class AlertResponse(BaseResponseModel):
    lago_id: str
    lago_organization_id: str
    external_subscription_id: Optional[str]
    lago_wallet_id: Optional[str]
    wallet_code: Optional[str]
    alert_type: str
    code: str
    name: str
    direction: str
    previous_value: int
    last_processed_at: str
    thresholds: AlertThresholdResponseList
    created_at: str
    billable_metric: Optional[BillableMetricResponse]
