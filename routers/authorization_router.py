from typing import Annotated

from fastapi import APIRouter, Depends

from repositories.auth_repository import AuthRepository
from schemas.auth_schemas import SPhoneCheck, SPhoneAdd

router = APIRouter(
    prefix="/auth",
    tags=["Авторизация"],
)

@router.post("")
async def add_phone(phone: Annotated[SPhoneAdd, Depends()],) -> int:
    phone_id = await AuthRepository.add_user(phone)
    return phone_id

@router.post("/check_code")
async def check_code(data: Annotated[SPhoneCheck, Depends()],) -> dict:
    user_auth_info = await AuthRepository.check_user(data)
    return user_auth_info