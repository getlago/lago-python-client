from typing import Any, Dict, List, Optional

from ..base_model import BaseResponseModel


class PlanEntitlementPrivilegeResponse(BaseResponseModel):
    code: Optional[str]
    name: Optional[str]
    value_type: Optional[str]
    config: Optional[Dict[str, Any]]
    value: Any


class PlanEntitlementPrivilegesResponse(BaseResponseModel):
    __root__: List[PlanEntitlementPrivilegeResponse]


class PlanEntitlementResponse(BaseResponseModel):
    code: Optional[str]
    name: Optional[str]
    description: Optional[str]
    privileges: Optional[PlanEntitlementPrivilegesResponse]


class PlanEntitlementsResponse(BaseResponseModel):
    __root__: List[PlanEntitlementResponse]
