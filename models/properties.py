from pydantic import BaseModel
from typing import Optional

class Properties(BaseModel):
    property_id: Optional[int] = None
    host_id: Optional[int] = None
    destination_id: Optional[int] = None
    title: Optional[str] = None
    description: Optional[str] = None
    base_price: Optional[float] = None
    property_type: Optional[str] = None
    max_guests: Optional[int] = None
    bedrooms: Optional[int] = None
    bathrooms: Optional[int] = None
    property_latitude: Optional[float] = None
    property_longitude: Optional[float] = None
    created_at: Optional[str] = None