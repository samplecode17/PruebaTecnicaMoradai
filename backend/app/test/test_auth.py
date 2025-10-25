import pytest
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from .test_main import session
from app.api.v1.auth import *
from app.crud.user import create_user
from app.schemas.user import UserBase

#correct login
@pytest.mark.asyncio
async def test_login_for_access_token_success(session):
    # create a user
    user_data = UserBase(
        username="admin",
        email="example@example.com",
        password="secure123"
    )
    await create_user(session, user_data)

    # create login form data
    form_data = OAuth2PasswordRequestForm(
        username=user_data.username,
        password=user_data.password,
        scope="",
        grant_type="",
        client_id=None,
        client_secret=None,
    )

    # call login function
    response = await login_for_access_token(form_data=form_data, session=session)

    # check if response and cookie are correct
    assert response.status_code == 200
    assert "set-cookie" in response.headers
    assert 'Authorization="Bearer' in response.headers["set-cookie"]
    # check the message in response body
    assert "ve successfully logged in. Welcome back!" in str(response.body)



#login with wrong pasword
@pytest.mark.asyncio
async def test_login_for_access_token_wrong_password(session):
    # create a user
    user_data = UserBase(
        username="wrong_pass_user",
        email="wrongpass@example.com",
        password="secure123"
    )
    await create_user(session, user_data)

    # create form data with wrong password
    form_data = OAuth2PasswordRequestForm(
        username=user_data.username,
        password="wrongpassword",
        scope="",
        grant_type="",
        client_id=None,
        client_secret=None,
    )

    # expect http exception for invalid credentials
    with pytest.raises(HTTPException) as exc_info:
        await login_for_access_token(form_data=form_data, session=session)

    # check the exception details
    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == "Incorrect username or password"



@pytest.mark.asyncio
async def test_login_for_access_token_nonexistent_user(session):
    # create form data for non-existent user
    form_data = OAuth2PasswordRequestForm(
        username="unexistent_user",
        password="somepassword",
        scope="",
        grant_type="",
        client_id=None,
        client_secret=None,
    )

    # expect http exception for user not found
    with pytest.raises(HTTPException) as exc_info:
        await login_for_access_token(form_data=form_data, session=session)

    # check the exception details
    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == "Incorrect username or password"
    
    
#read my self
@pytest.mark.asyncio
async def test_read_users_me_success(session):
    # create a user
    user_data = UserBase(
        username="user",
        email="user@example.com",
        password="secure123"
    )
    user = await create_user(session, user_data)

    # call read_users_me with the current user
    response = await read_users_me(current_user=user)

    # check that the response has correct fields
    assert isinstance(response, User)
    assert response.username == user_data.username
    assert response.email == user_data.email
    assert response.id == user.id

