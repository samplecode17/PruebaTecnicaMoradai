from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class UserBase(BaseModel):
    username: Optional[str] = "admin"
    password: Optional[str] = "password"
    email: Optional[str] = "random@random.com"

class UserRead(UserBase):
    id: UUID
    class Config:
        orm_mode = True # allows returning SQLModel instances directly
