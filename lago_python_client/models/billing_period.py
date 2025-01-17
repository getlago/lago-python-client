from typing import List

from lago_python_client.base_model import BaseResponseModel


class BillingPeriodResponse(BaseResponseModel):
    lago_subscription_id: str
    external_subscription_id: str
    lago_plan_id: str
    subscription_from_datetime: str
    subscription_to_datetime: str
    charges_from_datetime: str
    charges_to_datetime: str
    invoicing_reason: str


class BillingPeriodsResponse(BaseResponseModel):
    __root__: List[BillingPeriodResponse]
