from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional
from uuid import UUID
from string  import ascii_uppercase, digits
from random import choices

#Generate 10 keys random code
def generate_random_code(length: int = 10) -> str:
    characters = ascii_uppercase + digits
    return ''.join(choices(characters, k=length))


#Referral code model
class ReferralCode(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    code: str = Field(default_factory=generate_random_code, unique=True, index=True)
    user_id: Optional[UUID] = Field(default=None, foreign_key="user.id", nullable=True)
    created_at: Optional[datetime] = Field(default_factory=datetime.now())

    # Relationship: referral code belongs to one user
    user: Optional["User"] = Relationship(back_populates="referral_codes")