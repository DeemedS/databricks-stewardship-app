from pydantic import BaseModel
from typing import Optional

class Payments(BaseModel):
    payment_id: Optional[int] = None
    booking_id: Optional[int] = None
    amount: Optional[str] = None
    payment_method: Optional[str] = None
    status: Optional[str] = None
    payment_date: Optional[str] = None