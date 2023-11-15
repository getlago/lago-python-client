from typing import List, Optional

from ..base_model import BaseModel, BaseResponseModel


class MrrResponse(BaseResponseModel):
    amount_cents: Optional[int]
    currency: Optional[str]
    month: str


class MrrsResponse(BaseResponseModel):
    __root__: List[MrrResponse]
