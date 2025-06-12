from typing import List, Optional

from lago_python_client.base_model import BaseModel

from ..base_model import BaseResponseModel

class InvoiceCustomSectionResponse(BaseResponseModel):
    lago_id: Optional[str]
    code: Optional[str]
    name: Optional[str]
    description: Optional[str]
    details: Optional[str]
    display_name: Optional[str]
    applied_to_organization: Optional[bool] # Deprecated


class InvoiceCustomSectionsResponseList(BaseResponseModel):
    __root__: List[InvoiceCustomSectionResponse]
