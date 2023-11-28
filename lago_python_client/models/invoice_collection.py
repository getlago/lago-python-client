from typing import List, Optional

from ..base_model import BaseModel, BaseResponseModel


class InvoiceCollectionResponse(BaseResponseModel):
    amount_cents: int
    currency: Optional[str]
    month: str
    invoices_count: int
    payment_status: Optional[str]


class InvoiceCollectionsResponse(BaseResponseModel):
    __root__: List[InvoiceCollectionResponse]
