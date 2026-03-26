from pydantic import BaseModel
from typing import Optional

class Page_views(BaseModel):
    device_type: Optional[str] = None
    page_url: Optional[str] = None
    property_id: Optional[int] = None
    referrer: Optional[str] = None
    timestamp: Optional[str] = None
    user_id: Optional[int] = None
    view_id: Optional[int] = None