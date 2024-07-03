from typing import Union

from sqlalchemy import select
import random

from db.database import new_session, TaskOrm, AuthOrm
from schemas.auth_schemas import SPhoneAdd, SPhoneCheck
from schemas.task_schemas import STaskAdd, STask


class AuthRepository:
    @classmethod
    async def add_user(cls, auth_phone: SPhoneAdd) -> int:
        phone_validation_list = random.sample("123456789", 4)
        phone_validation_token = "".join(phone_validation_list)
        print(phone_validation_token)
        async with new_session() as session:
            auth_dict = auth_phone.model_dump()
            auth_dict['phone_validation_token'] = phone_validation_token
            auth_phone = AuthOrm(**auth_dict)
            session.add(auth_phone)
            await session.flush()
            await session.commit()
            return auth_phone.id

    @classmethod
    async def check_user(cls, data: SPhoneCheck) -> dict:
        async with new_session() as session:
            data = data.model_dump()
            res = await session.execute(select(AuthOrm).where((AuthOrm.id == data['id']) and (AuthOrm.phone_validation_token == data['code'])))
            await session.commit()
            res = res.scalar_one()
            return {
                'id': res.id,
                'phone_validation_token': res.phone_validation_token
            }

