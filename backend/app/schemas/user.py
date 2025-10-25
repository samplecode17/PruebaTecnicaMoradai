from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class UserBase(BaseModel):
    username: Optional[str] = "admin"
    password: Optional[str] = "password"
    email: Optional[str] = "random@random.com"

class UserRead(UserBase):
    id: UUID
    model_config = {
        "from_attributes": True
    }

class UserCreationResponse(BaseModel):
    response: str
