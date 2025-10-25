import pytest
from fastapi import HTTPException
from app.api.v1.referalcode import *
from app.schemas.referalcode import *
from app.schemas.user import *
from app.api.v1.auth import *
from .test_main import session
from app.api.v1.user import create as create_user
from app.crud.user import get_user_by_username

# create a referalcode correctly
@pytest.mark.asyncio
async def test_create_referalcode(session):
    # user data
    user_data = UserBase(
        username="test",
        email="usuario@example.com",
        password="secure1234"
    )
    # create user
    await create_user(user_data, session)
    # get user by username
    user = await get_user_by_username(session, user_data.username)
  
    code = ReferralCodeBase(user_id=user.id)
    result = await create(code, session)
    
    
    # check user fields
    assert result == ReferralCodeResponse(response="referralcode created")

# create a referral code without an userid
@pytest.mark.asyncio
async def test_create_referralcode_without_userid(session):
    code = ReferralCodeBase()
    
    with pytest.raises(HTTPException) as exec_info:
      await create(code, session)
    assert exec_info.value.status_code==400
    assert "user_id is required for creating a referral code" in str(exec_info.value.detail).lower()

# create a referral code already exists
@pytest.mark.asyncio
async def test_create_referralcode_already_exists(session):
    user_data = UserBase(
        username="test",
        email="usuario@example.com",
        password="secure1234"
    )
    # create user
    await create_user(user_data, session)
    # get user by username
    user = await get_user_by_username(session, user_data.username)
    #create the first referral code
    code = ReferralCodeBase(user_id=user.id, code="HOLA")
    await create(code, session)
    #create the second referral code with the same data
    with pytest.raises(HTTPException) as exec_info:
      await create(code, session)
    assert exec_info.value.status_code==400
    assert "integrity error: referral code already exists" in str(exec_info.value.detail).lower()

#create a referral code with unexistent user_id
@pytest.mark.asyncio
async def test_create_referralcode_with_unexistent_user_id(session):
    
    code = ReferralCodeBase(user_id=UUID("0c2b81d0-d43d-4823-b734-98aff387f559"), code="HOLA")
    #create the referral code with false UUID
    with pytest.raises(HTTPException) as exec_info:
      await create(code, session)
    assert exec_info.value.status_code==404
    assert "user with id 0c2b81d0-d43d-4823-b734-98aff387f559" in str(exec_info.value.detail).lower()

    
#read correctly a referral code
@pytest.mark.asyncio
async def test_read_a_referralcode_correctly(session):
    user_data = UserBase(
        username="test",
        email="usuario@example.com",
        password="secure1234"
    )
    # create user
    await create_user(user_data, session)
    # get user by username
    user = await get_user_by_username(session, user_data.username)
  
    code = ReferralCodeBase(user_id=user.id, code="HOLA")
    await create(code, session)
    #read the referal code
    result= await read(1,session)
    
    assert result.user_id == user.id
    assert result.code==code.code

#read unexistent referral code
@pytest.mark.asyncio
async def test_read_unexistent_referralcode(session):
    with pytest.raises(HTTPException) as exec_info:
        await read(2,session)
    assert exec_info.value.status_code==404
    assert "referal code not found" in str(exec_info.value.detail).lower()

# update a referalcode correctly
@pytest.mark.asyncio
async def test_update_referalcode(session):
    # user data
    user_data = UserBase(
        username="test",
        email="usuario@example.com",
        password="secure1234"
    )
    # create user
    await create_user(user_data, session)
    # get user by username
    user = await get_user_by_username(session, user_data.username)
    
    #create the referal code that we want to edit later
    code = ReferralCodeBase(user_id=user.id)
    await create(code, session)
    
    
    updated_code = ReferralCodeBase(code="HOLA")
    result = await update(1,updated_code,session)
    
    assert result == ReferralCodeResponse(response="referralcode updated")


#update the code with the data that already exist in another code
@pytest.mark.asyncio
async def test_update_referralcode_already_exists(session):
    user_data = UserBase(
        username="test",
        email="usuario@example.com",
        password="secure1234"
    )
    # create user
    await create_user(user_data, session)
    user = await get_user_by_username(session, user_data.username)
    #create the first referral code
    code = ReferralCodeBase(user_id=user.id,code="HOLA")
    await create(code, session)
    #update the referral code with the same data
    code = ReferralCodeBase(code="HOLA")
    with pytest.raises(HTTPException) as exec_info:
      await update(1,code,session)
    assert exec_info.value.status_code==400
    assert "integrity error: referral code already exists" in str(exec_info.value.detail).lower()

#update a referral code with unexistent user_id
@pytest.mark.asyncio
async def test_update_referralcode_with_unexistent_user_id(session):
    user_data = UserBase(
        username="test",
        email="usuario@example.com",
        password="secure1234"
    )
    # create user
    await create_user(user_data, session)
    # get user by username
    user = await get_user_by_username(session, user_data.username)
    #create the first referral code
    code = ReferralCodeBase(user_id=user.id, code="HOLA")
    await create(code, session)
    
    code = ReferralCodeBase(user_id=UUID("0c2b81d0-d43d-4823-b734-98aff387f559"), code="HOLA")
    #update the referral code with false UUID
    with pytest.raises(HTTPException) as exec_info:
      await update(1,code, session)
    assert exec_info.value.status_code==400

#update unexistent referral code
@pytest.mark.asyncio
async def test_update_unexistent_referralcode(session):
    with pytest.raises(HTTPException) as exec_info:
        await update(77,ReferralCodeBase(),session)
    assert exec_info.value.status_code==404
    assert "referralcode does not exist" in str(exec_info.value.detail).lower()




@pytest.mark.asyncio
async def test_delete(session):
    # create user
    user_data = UserBase(
        username="test",
        email="usuario@example.com",
        password="secure1234"
    )
    await create_user(user_data, session)
    # get user by username
    user = await get_user_by_username(session, user_data.username)
    #create the first referral code
    code = ReferralCodeBase(user_id=user.id, code="HOLA")
    await create(code, session)
    response = await delete(1, session=session)
    # check response
    assert response == {"ok": True}


@pytest.mark.asyncio
async def test_delete_not_found(session):
    # try to delete non-existing referal code
    with pytest.raises(HTTPException) as exc_info:
        await delete(3, session=session)
    # check 400 code
    assert exc_info.value.status_code == 400
