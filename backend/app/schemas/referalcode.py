from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class ReferralCodeBase(BaseModel):
    user_id: Optional[UUID] = None 
    
class ReferralCodeCreate(ReferralCodeBase):
    pass 

class ReferralCodeRead(ReferralCodeBase):
    id: int
    code: str
    created_at: datetime

    class Config:
        orm_mode = True  # allows returning SQLModel instances directly
        
class ReferralCodeUpdate(ReferralCodeBase):
    code: Optional[str]
