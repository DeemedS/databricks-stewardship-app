from pydantic import BaseModel
from typing import Optional

class Booking_updates(BaseModel):
    booking_id: Optional[int] = None
    booking_update_id: Optional[int] = None
    check_in: Optional[str] = None
    check_out: Optional[str] = None
    created_at: Optional[str] = None
    guests_count: Optional[int] = None
    property_id: Optional[int] = None
    status: Optional[str] = None
    total_amount: Optional[float] = None
    updated_at: Optional[str] = None
    user_id: Optional[int] = None