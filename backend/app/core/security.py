import jwt
from app.core.config import settings
from app.crud.user import get_user_by_username
from datetime import datetime, timedelta, timezone
from jwt.exceptions import InvalidTokenError
from sqlmodel.ext.asyncio.session import AsyncSession
#from passlib.context import CryptContext
from datetime import datetime, timedelta
from fastapi import HTTPException, status, Depends,Request
from app.session import get_session
from fastapi.security import OAuth2, OAuth2PasswordBearer
from fastapi.security.utils import get_authorization_scheme_param
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel
from typing import Optional
from app.models.user import User


# get secret key settings from the settings
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES


#pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto") -> in this case no need to encrypt the password
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

def verify_password(plain_password, password):
    #return pwd_context.verify(plain_password, password)
    #simple password verification (simulation encrypted verification passwordz)
    return plain_password == password


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    # copy data to encode
    to_encode = data.copy()
    # calculate expiration time
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    # encode jwt token
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def authenticate_user(session: AsyncSession, username: str, password: str) -> Optional[User]:
    # fetch user by username
    user = await get_user_by_username(session, username)
    print(password)
    # verify password
    if user and verify_password(password, user.password):
        return user
    return None


class OAuth2PasswordBearerCookie(OAuth2):
    # custom oauth2 class to read token from cookies
    def __init__(
        self,
        token_url: str,
        scheme_name: str = None,
        scopes: dict = None,
        auto_error: bool = True,
    ):
        # default empty scopes
        if not scopes:
            scopes = {}
        # define password flow
        flows = OAuthFlowsModel(password={"tokenUrl": token_url, "scopes": scopes})
        super().__init__(flows=flows, scheme_name=scheme_name, auto_error=auto_error)

    async def __call__(self, request: Request) -> Optional[str]:
        # get authorization token from cookies
        authorization: str = request.cookies.get("Authorization")
        scheme, param = get_authorization_scheme_param(authorization)

        # check if token is present and is bearer
        if not authorization or scheme.lower() != "bearer":
            if self.auto_error:
                # raise exception if token missing or invalid
                raise HTTPException(
                    status_code=401,
                    detail="Not authenticated",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            else:
                return None

        # return token value
        return param


# initialize custom security
security = OAuth2PasswordBearerCookie(token_url="/auth/token")

async def get_current_user(
    token: str = Depends(security),
    session: AsyncSession = Depends(get_session)
) -> User:
    # print token for debugging
    print(token)
    # define exception for invalid credentials
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # decode jwt token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        # check if username exists
        if username is None:
            raise credentials_exception
    except InvalidTokenError:
        # raise exception if token invalid
        raise credentials_exception
    try:
        # fetch user from db
        user = await get_user_by_username(session, username)
    except:
        # raise exception if error occurs
        raise credentials_exception
    if user is None:
        # raise exception if user not found
        raise credentials_exception
    # return authenticated user
    return user