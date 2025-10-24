from sqlmodel import select
from fastapi import HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession
from app.models.referalcode import ReferralCode
from app.schemas.referalcode import ReferralCodeBase, ReferralCodeUpdate
from uuid import UUID





#create referral code
async def create_referralcode(session: AsyncSession, referralcode_create: ReferralCodeBase)-> ReferralCode:
  
  # extract only the fields that were actually provided in the get request to a dictionary
  db_referralcode = ReferralCode(**referralcode_create.model_dump(exclude_unset=True))
  await session.commit()
  await session.refresh(db_referralcode)
  return db_referralcode


#get all referral codes
async def get_referralcodes(session: AsyncSession)-> list[ReferralCode]:
  result = await session.exec(select(ReferralCode))
  return result.all()


#get referral code
async def get_referralcode(session: AsyncSession, referralcode_id: int)-> ReferralCode:
  return await session.get(ReferralCode,referralcode_id)


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
  await session.commit()
  await session.refresh(db_referralcode)
  return db_referralcode


#delete referral code
async def delete_referralcode(session: AsyncSession, referralcode_id: UUID) -> None:
    db_referralcode = await get_referralcode(session, referralcode_id)
    if db_referralcode is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Referral code does not exist"
        )
    await session.delete(db_referralcode)
    await session.commit()