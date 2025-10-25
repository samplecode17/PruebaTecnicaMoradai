from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from datetime import timedelta
from app.core.security import authenticate_user, create_access_token, get_current_user, ACCESS_TOKEN_EXPIRE_MINUTES, verify_password
from app.schemas.user import UserRead
from app.models.user import User
from app.session import get_session
from sqlmodel.ext.asyncio.session import AsyncSession

router = APIRouter(tags=["Auth"], prefix="/auth")

@router.post("/token", summary="Login y obtención de token de acceso")
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_session)
):
    """
    Endpoint para autenticar al usuario mediante username y password, 
    y obtener un token JWT para acceso autenticado.
    
    Retorna un cookie HTTP-only con el token de acceso.
    """
    user = await authenticate_user(session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    token = jsonable_encoder(access_token)
    content = {"message": "You've successfully logged in. Welcome back!"}
    response = JSONResponse(content=content)
    response.set_cookie(
        "Authorization",
        value=f"Bearer {token}",
        httponly=True,
        max_age=1800,
        expires=1800,
        samesite="None",
        secure=True,  # Cambiar a True si usas HTTPS en producción

    )
    return response

@router.get("/me", response_model=UserRead, summary="Obtener información del usuario autenticado")
async def read_users_me(current_user: User = Depends(get_current_user)):
    """
    Devuelve los datos completos del usuario autenticado.
    """
    return current_user

