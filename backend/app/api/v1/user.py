from fastapi import APIRouter, HTTPException, Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from app.session import get_session
from app.schemas.user import *
from app.crud.user import *
from app.models.user import User




router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", summary="Crear un nuevo usuario", response_model=UserCreationResponse)
async def create(
    user_create: UserBase,
    session: AsyncSession = Depends(get_session)
):
  """
    Crea un nuevo usuario en la base de datos.

    Retorna un mensaje indicando el resultado de la operación.
  """
  result = await create_user(session, user_create)
  #if the user is not created
  if not result:
      raise HTTPException(status_code=404, detail="User not created")
  return UserCreationResponse(response="User created")


@router.get("/", response_model=list[UserRead], summary="Listar todos los usuarios")
async def read_all(
    session: AsyncSession = Depends(get_session),
):
    """
    Obtiene la lista de todos los usuarios accesible para el usuario autenticado.
    """
    return await get_users(session)



@router.get("/{user_id}", response_model=UserRead, summary="Obtener detalles de usuario")
async def read(
    user_id: UUID,
    session: AsyncSession = Depends(get_session)
):
    """
    Obtiene la información de un usuario específico para el usuario autenticado.
    """
    user = await get_user(session, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/{user_id}", response_model=UserRead, summary="Actualizar información de usuario")
async def update(
    user_id: UUID,
    user_update: UserBase,
    session: AsyncSession = Depends(get_session)
):
    """
    Actualiza los datos de un usuario específico.
    """
    return await update_user(session, user_id, user_update)

async def delete(
    user_id: UUID,
    session: AsyncSession = Depends(get_session)
):
    """
    Elimina un usuario específico de la base de datos.
    """
    await delete_user(session, user_id)
    return {"ok": True}