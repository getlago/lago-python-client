from pydantic import BaseModel, Field
from typing import Optional

class InvoiceItemResponse(BaseModel):
    lago_id: Optional[str]
    type: Optional[str]
    code: Optional[str]
    name: Optional[str]
