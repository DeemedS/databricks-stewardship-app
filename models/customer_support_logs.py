from pydantic import BaseModel
from typing import Optional

class Customer_support_logs(BaseModel):
    created_at: Optional[str] = None
    messages: Optional[str] = None
    support_agent_id: Optional[str] = None
    ticket_id: Optional[str] = None
    user_id: Optional[int] = None