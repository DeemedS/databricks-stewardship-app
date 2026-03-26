from pydantic import BaseModel
from typing import Optional

class Users(BaseModel):
    user_id: Optional[int] = None
    email: Optional[str] = None
    name: Optional[str] = None
    country: Optional[str] = None
    user_type: Optional[str] = None
    created_at: Optional[str] = None
    is_business: Optional[bool] = None
    company_name: Optional[str] = None