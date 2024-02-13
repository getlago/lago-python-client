from typing import Optional

from lago_python_client.base_model import BaseModel

from ..base_model import BaseResponseModel


class Group(BaseModel):
    lago_id: Optional[str]
    key: Optional[str]
    value: Optional[str]


class GroupResponse(BaseResponseModel):
    lago_id: str
    key: str
    value: str
