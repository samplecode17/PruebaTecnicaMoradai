from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional, List
from uuid import UUID

# User model
class User(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    username: Optional[str]
    email: Optional[str]
    password: Optional[str]
    created_at: Optional[datetime] = Field(default_factory=datetime.now())

    # Relationship: one to much -> User->ReferralCode
    referral_codes: List["ReferralCode"] = Relationship(back_populates="user")