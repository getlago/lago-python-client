from typing import Optional

from lago_python_client.base_model import BaseModel


class PaymentTerm(BaseModel):
    term_type: str
    days: Optional[int]
    day_of_month: Optional[int]
    month_offset: Optional[int]
