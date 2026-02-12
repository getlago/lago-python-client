from typing import Optional

from lago_python_client.base_model import BaseModel

from ..base_model import BaseResponseModel


class PaymentMethod(BaseModel):
    payment_method_type: Optional[str]
    payment_method_id: Optional[str]


class PaymentMethodResponse(BaseResponseModel):
    lago_id: str
    is_default: Optional[bool]
    payment_provider_code: Optional[str]
    payment_provider_name: Optional[str]
    payment_provider_type: Optional[str]
    provider_method_id: Optional[str]
    created_at: Optional[str]
