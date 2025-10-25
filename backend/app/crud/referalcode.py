from sqlmodel import select
from fastapi import HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession
from app.models.referalcode import ReferralCode
from app.schemas.referalcode import ReferralCodeBase, ReferralCodeUpdate, ReferralCodeVerification
from uuid import UUID
from sqlalchemy.exc import IntegrityError, SQLAlchemyError




#create referral code
async def create_referralcode(session: AsyncSession, referralcode_create: ReferralCodeBase)-> ReferralCode:
  
  #validate that a user_id comes
  if not referralcode_create.user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="user_id is required for creating a referral code"
        )
  # extract only the fields that were actually provided in the get request to a dictionary
  db_referralcode = ReferralCode(**referralcode_create.model_dump(exclude_unset=True))
  session.add(db_referralcode)
  try:
    await session.commit()
    await session.refresh(db_referralcode)
    return db_referralcode
  except IntegrityError:
    # Rollback in case of an integrity error (duplicate or invalid foreign key)
    await session.rollback()
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Integrity error: referral code already exists"
    )
  except SQLAlchemyError as e:
        # Rollback in case of any other database error
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )

    

#get all referral codes
async def get_referralcodes(session: AsyncSession)-> list[ReferralCode]:
  try:
      result = await session.exec(select(ReferralCode))
      return result.all()
  except SQLAlchemyError as e:
      raise HTTPException(
          status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
          detail=f"Database error: {str(e)}"
      )


#get referral code
async def get_referralcode(session: AsyncSession, referralcode_id: int)-> ReferralCode | None:
  try:
      return await session.get(ReferralCode,referralcode_id)
  except SQLAlchemyError as e:
      raise HTTPException(
          status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
          detail=f"Database error: {str(e)}"
      )


#verify referral code exists
async def verify_referralcode(session: AsyncSession, code: str) -> ReferralCodeVerification:
    try:
        result = await session.exec(
            select(ReferralCode).where(ReferralCode.code == code)
        )
        referral = result.scalar_one_or_none()
        return ReferralCodeVerification(exists=bool(referral))
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )
        
#update referralcode
async def update_referralcode(session: AsyncSession, referralcode_id: int, referralcode_update: ReferralCodeUpdate) -> ReferralCode:
  db_referralcode = get_referralcode(session, referralcode_id)
  #referralcode exists?
  if db_referralcode is None:
    #if not exists
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="referralcode does not exist"
    )
  # extract only the fields that were actually provided in the update request to a dictionary
  referralcode_data = referralcode_update.model_dump(exclude_unset=True)
  for key, value in referralcode_data.items():
    setattr(db_referralcode, key, value)
  #update the referralcode        
  session.add(db_referralcode)
  #
  try:
    await session.commit()
    await session.refresh(db_referralcode)
    return db_referralcode
  except IntegrityError:
    # Rollback in case of an integrity error (duplicate or invalid foreign key)
    await session.rollback()
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Integrity error: referral code already exists"
    )
  except SQLAlchemyError as e:
        # Rollback in case of any other database error
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )


#delete referral code
async def delete_referralcode(session: AsyncSession, referralcode_id: UUID) -> None:
    db_referralcode = await get_referralcode(session, referralcode_id)
    if db_referralcode is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Referral code does not exist"
        )
    try:  
      await session.delete(db_referralcode)
      await session.commit()
    except SQLAlchemyError as e:
        # Rollback in case of any other database error
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )
