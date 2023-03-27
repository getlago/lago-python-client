from typing import Optional

from ..base_model import BaseResponseModel


class InvoiceItemResponse(BaseResponseModel):
    lago_id: Optional[str]
    type: Optional[str]
    code: Optional[str]
    name: Optional[str]
