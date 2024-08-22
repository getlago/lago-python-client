from typing import Any, Dict, List, Optional, Union

from lago_python_client.base_model import BaseModel

from ..base_model import BaseResponseModel


class ErrorDetailResponse(BaseModel):
    organization_id: str
    error_code: str
    details: Optional[Dict[str, Any]]


class ErrorDetailsResponse(BaseResponseModel):
    __root__: List[ErrorDetailResponse]
