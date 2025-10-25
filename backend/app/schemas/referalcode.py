from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class ReferralCodeBase(BaseModel):
    user_id: Optional[UUID] = None
    code: Optional[str] = None
    

class ReferralCodeRead(ReferralCodeBase):
    id: int
    code: str
    created_at: datetime


    # allows returning SQLModel instances directly
    model_config = {
        "from_attributes": True
    } 
class ReferralCodeVerification(BaseModel):
    exists: bool
    
class ReferralCodeResponse(BaseModel):
    response: str