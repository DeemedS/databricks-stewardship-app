from pydantic import BaseModel
from typing import Optional

class Reviews(BaseModel):
    booking_id: Optional[int] = None
    comment: Optional[str] = None
    created_at: Optional[str] = None
    is_deleted: Optional[bool] = None
    property_id: Optional[int] = None
    rating: Optional[float] = None
    review_id: Optional[int] = None
    updated_at: Optional[str] = None
    user_id: Optional[int] = None