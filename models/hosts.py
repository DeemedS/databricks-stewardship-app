from pydantic import BaseModel
from typing import Optional

class Hosts(BaseModel):
    host_id: Optional[int] = None
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    is_verified: Optional[bool] = None
    is_active: Optional[bool] = None
    rating: Optional[float] = None
    country: Optional[str] = None
    joined_at: Optional[str] = None