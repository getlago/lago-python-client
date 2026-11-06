from typing import List, Optional

from ..base_model import BaseModel, BaseResponseModel


class UsageAttributionType(BaseModel):
    code: Optional[str]
    name: Optional[str]
    description: Optional[str]
    role: Optional[str]
    parent_code: Optional[str]
    attribution_keys: Optional[List[str]]


class UsageAttributionTypeResponse(BaseResponseModel):
    lago_id: str
    lago_organization_id: str
    code: str
    name: Optional[str]
    description: Optional[str]
    attribution_keys: List[str]
    role: str
    lago_parent_id: Optional[str]
    parent_code: Optional[str]
    created_at: str
    updated_at: str


class UsageAttributionTypesResponse(BaseResponseModel):
    __root__: List[UsageAttributionTypeResponse]
