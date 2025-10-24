from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional
from uuid import UUID

#Referral code model
class ReferralCode(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    code: str
    user_id: Optional[UUID] = Field(default=None, foreign_key="user.id", nullable=True)
    created_at: Optional[datetime] = Field(default_factory=datetime.now())

    # Relationship: referral code belongs to one user
    user: Optional["User"] = Relationship(back_populates="referral_codes")