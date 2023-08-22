from typing import Optional

from ..base_model import BaseResponseModel


class InvoiceItemResponse(BaseResponseModel):
    type: Optional[str]
    code: Optional[str]
    name: Optional[str]
    lago_id: Optional[str]
    item_type: Optional[str]
