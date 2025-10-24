from sqlmodel import select
from fastapi import HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession
from app.models.user import User
from app.schemas.user import UserBase
from uuid import UUID


#create user
async def create_user(session: AsyncSession, user_create: UserBase)-> User:
  
  # extract only the fields that were actually provided in the get request to a dictionary
  db_user = User(**user_create.model_dump(exclude_unset=True, exclude={"referral_code"}))
  query = select(User).where(
        (User.username == db_user.username) | (User.email == db_user.email)
  )
  result = await session.exec(query)
  #user already exists?
  existing_user = result.one_or_none()
  if existing_user:
        #if exists
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already created"
        )
  await session.commit()
  await session.refresh(db_user)
  return db_user


#get all users
async def get_users(session: AsyncSession)-> list[User]:
  result = await session.exec(select(User))
  return result.all()

#get user
async def get_user(session: AsyncSession, user_id: UUID)-> User | None:
  return await session.get(User, user_id)

#get user by username\
async def get_user_by_username(session: AsyncSession, username: str) -> User | None:
    #find the user
    statement = select(User).where(User.username == username)
    result = await session.exec(statement)
    return result.first()


#update user
async def update_user(session: AsyncSession, user_id: UUID, user_update: UserBase) -> User:
  db_user = get_user(session, user_id)
  #user exists?
  if db_user is None:
    #if not exists
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="User does not exist"
    )
  # extract only the fields that were actually provided in the update request to a dictionary
  user_data = user_update.model_dump(exclude_unset=True)
  for key, value in user_data.items():
    setattr(db_user, key, value)
  #update the user        
  session.add(db_user)
  await session.commit()
  await session.refresh(db_user)
  return db_user


#delete user
async def delete_user(session: AsyncSession, user_id: UUID) -> None:
    db_user = await get_user(session, user_id)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User does not exist"
        )
    await session.delete(db_user)
    await session.commit()
