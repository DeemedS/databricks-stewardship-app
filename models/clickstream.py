from pydantic import BaseModel
from typing import Optional

class Clickstream(BaseModel):
    event: Optional[str] = None
    metadata: Optional[str] = None
    property_id: Optional[int] = None
    timestamp: Optional[str] = None
    user_id: Optional[int] = None