from pydantic import BaseModel
from typing import Optional

class Destinations(BaseModel):
    destination_id: Optional[int] = None
    destination: Optional[str] = None
    country: Optional[str] = None
    state_or_province: Optional[str] = None
    state_or_province_code: Optional[str] = None
    description: Optional[str] = None