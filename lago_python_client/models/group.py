from typing import Optional

from pydantic import BaseModel


class Group(BaseModel):
    lago_id: Optional[str]
    key: Optional[str]
    value: Optional[str]


class GroupResponse(BaseModel):
    lago_id: str
    key: str
    value: str
