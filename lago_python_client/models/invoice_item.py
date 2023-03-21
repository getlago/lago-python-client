from typing import Optional

from pydantic import BaseModel


class InvoiceItemResponse(BaseModel):
    lago_id: Optional[str]
    type: Optional[str]
    code: Optional[str]
    name: Optional[str]
