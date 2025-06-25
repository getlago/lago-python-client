from typing import Optional

from lago_python_client.base_model import BaseModel

from ..base_model import BaseResponseModel


class ApiLog(BaseModel):
    api_version: str
    client: str
    http_method: str
    http_status: int
    request_body: dict
    logged_at: str
    request_origin: str
    created_at: str
    request_path: str
    request_response: Optional[dict]
    request_id: str


class ApiLogResponse(BaseResponseModel):
    request_id: str
    client: str
    http_method: str
    http_status: int
    request_origin: str
    request_path: str
    request_body: dict
    request_response: Optional[dict]
    api_version: str
    logged_at: str
    created_at: str
