import pytest
from fastapi import HTTPException
from app.api.v1.user import *
from app.crud.user import get_user_by_username
from app.schemas.user import *
from app.api.v1.auth import *
from .test_main import session


# create an user test
@pytest.mark.asyncio
async def test_create_user(session):
    # user data
    user_data = UserBase(
        username="test",
        email="usuario@example.com",
        password="secure1234"
    )
    # create user
    response = await create(user_data, session)
    # get user by username
    user = await get_user_by_username(session, user_data.username)
    # check response
    assert response == UserCreationResponse(response="User created")
    # check user fields
    assert user.username == user_data.username
    assert user.email == user_data.email


# create a user that already exists test
@pytest.mark.asyncio
async def test_create_same_user(session):
    # user data
    user_data = UserBase(
        username="test",
        email="usuario@example.com",
        password="secure1234"
    )
    # create user first time
    await create(user_data, session)
    # try to create the same user again
    with pytest.raises(HTTPException) as exc_info:
        await create(user_data, session)
    
    # check error code 400
    assert exc_info.value.status_code == 400
    # check error message
    assert "already" in str(exc_info.value.detail).lower()

@pytest.mark.asyncio
async def test_get_user(session):
    # user data
    user_data = UserBase(
        username="test",
        email="usuario@example.com",
        password="secure1234"
    )
    # create user
    await create(user_data, session)
    # get user by username
    user = await get_user_by_username(session, user_data.username)
    # call read endpoint
    response = await read(session=session, user_id=user.id)
    # expected result
    correct_result = UserRead(
        id=user.id,
        username=user.username,
        email=user.email,
        password=user.password,
        created_at=str(user.created_at)
    )
    # assert response
    assert response == correct_result


@pytest.mark.asyncio
async def test_get_unexistent_user(session):
    # fake user id
    false_user = UUID("123e4567-e89b-12d3-a456-426614174000")
    # try to read non-existing user
    with pytest.raises(HTTPException) as exc_info:
        await read(user_id=false_user, session=session)
    # check 404 code
    assert exc_info.value.status_code == 404


@pytest.mark.asyncio
async def test_update_user(session):
    # create user
    user_data = UserBase(
        username="test",
        email="usuario@example.com",
        password="secure1234"
    )
    await create(user_data, session)
    # update data
    update_data = UserBase(password="1234secure")
    # get user
    user = await get_user_by_username(session, user_data.username)
    # update user
    await update(session=session, user_id=user.id, user_update=update_data)
    # read updated user
    user = await read(session=session, user_id=user.id)
    # check password updated
    assert user.password == update_data.password


@pytest.mark.asyncio
async def test_update_user_with_other_existent_user_data(session):
    # create first user
    user_data = UserBase(
        username="test",
        email="usuario@example.com",
        password="secure1234"
    )
    await create(user_data, session)
    # create second user
    user_data1 = UserBase(
        username="test1",
        email="usuario1@example.com",
        password="secure1234"
    )
    await create(user_data1, session)
    # try to update first user with second user's data
    update_data = UserBase(username="test1")
    user = await get_user_by_username(session, user_data.username)
    # expect 400 error
    with pytest.raises(HTTPException) as exc_info:
        await update(session=session, user_id=user.id, user_update=update_data)
    assert exc_info.value.status_code == 400


@pytest.mark.asyncio
async def test_update_unexistent_user(session):
    # update data
    update_data = UserBase(password="secure1234")
    # fake user id
    false_user = UUID("123e4567-e89b-12d3-a456-426614174000")
    # try to update non-existing user
    with pytest.raises(HTTPException) as exc_info:
        await update(session=session, user_id=false_user, user_update=update_data)
    # check 400 code
    assert exc_info.value.status_code == 400


@pytest.mark.asyncio
async def test_delete(session):
    # create user
    user_data = UserBase(
        username="test",
        email="usuario@example.com",
        password="secure1234"
    )
    await create(user_data, session)
    # get user
    user = await get_user_by_username(session, user_data.username)
    # delete user
    response = await delete(user_id=user.id, session=session)
    # check response
    assert response == {"ok": True}


@pytest.mark.asyncio
async def test_delete_not_found(session):
    # fake user id
    false_user = UUID("123e4567-e89b-12d3-a456-426614174000")
    # try to delete non-existing user
    with pytest.raises(HTTPException) as exc_info:
        await delete(user_id=false_user, session=session)
    # check 400 code
    assert exc_info.value.status_code == 400
