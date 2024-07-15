from typing import Dict, List, Optional

from ..base_model import BaseResponseModel


class InvoiceItemResponse(BaseResponseModel):
    type: Optional[str]
    code: Optional[str]
    name: Optional[str]
    invoice_display_name: Optional[str]
    filter_invoice_display_name: Optional[str]
    filters: Optional[Dict[str, List[str]]]
    lago_item_id: Optional[str]
    item_type: Optional[str]
    grouped_by: Optional[Dict[str, str]]
