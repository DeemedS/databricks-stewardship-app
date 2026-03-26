from pydantic import BaseModel
from typing import Optional

class Bookings(BaseModel):
    booking_id: Optional[int] = None
    user_id: Optional[int] = None
    property_id: Optional[int] = None
    check_in: Optional[str] = None
    check_out: Optional[str] = None
    guests_count: Optional[int] = None
    total_amount: Optional[float] = None
    status: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None