from fastapi import APIRouter, HTTPException, Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from app.session import get_session
from app.schemas.referalcode import *
from app.crud.referalcode import *
from app.core.security import get_current_user
from app.models.user import User


router = APIRouter(prefix="/referalcodes", tags=["ReferralCodes"])


@router.post("/", response_model=ReferralCodeResponse, summary="Crear un codigo de referido")
async def create(
    referralcode_create: ReferralCodeBase,
    session: AsyncSession = Depends(get_session),
    _: User = Depends(get_current_user),#need to be loged in
):
    """
    Crea un nuevo codigo de referido con los datos proporcionados.

    Retorna un mensaje de éxito si el codigo de referido fue creado correctamente.
    """
    result = await create_referralcode(session, referralcode_create)
    if not result:
        raise HTTPException(status_code=404, detail="Game not created")
    return ReferralCodeResponse(response="referralcode created")


@router.get("/", response_model=list[ReferralCodeRead], summary="Obtener todos los codigos de referido")
async def read_all(
    session: AsyncSession = Depends(get_session)
):
    """
    Devuelve todos los codigos de referido disponibles.
    """
    return await get_referralcodes(session)


@router.get("/{referralcode_id}", response_model=ReferralCodeRead, summary="Obtener detalles de un codigo de referido")
async def read(
    referralcode_id: int,
    session: AsyncSession = Depends(get_session)
):
    """
    Devuelve los detalles de un codigo de referido específico según su ID.
    """
    referralcode = await get_referralcode(session, referralcode_id)
    if not referralcode:
        raise HTTPException(status_code=404, detail="Referal code not found")
    return ReferralCodeRead.model_validate(referralcode)


@router.get("/verify/{referralcode}", response_model=ReferralCodeVerification, summary="Verificar el codigo de referido")
async def verify(
    referralcode: str,
    session: AsyncSession = Depends(get_session)
):
    """
    Devuelve si el codigo de referido existe mediante el codigo.
    """
    referralcode = await verify_referralcode(session, referralcode)
    return referralcode
  
  
@router.put("/{referralcode_id}", response_model=ReferralCodeResponse, summary="Actualizar un codigo de referido existente")
async def update(
    referralcode_id: int,
    referralcode_update: ReferralCodeBase,
    session: AsyncSession = Depends(get_session)
):
    """
    Actualiza un código de referido con los nuevos datos proporcionados.

    Lanza un error si el código de referido no existe.
    """
    result = await update_referralcode(session, referralcode_id, referralcode_update)
    if not result:
        raise HTTPException(status_code=404, detail="Game not found")
    return ReferralCodeResponse(response="referralcode updated")



@router.delete("/{referralcode_id}", summary="Eliminar un código de referido")
async def delete(
    referralcode_id: int,
    session: AsyncSession = Depends(get_session),
    _: User = Depends(get_current_user), #need to be loged in
):
    """
    Elimina un código de referido por su ID. Esta acción no se puede deshacer.
    """
    await delete_referralcode(session, referralcode_id)
    return {"ok": True}