from typing import Optional

from pydantic import BaseModel, ConfigDict


class SPhoneAdd(BaseModel):
    phone: str


class SPhoneCheck(BaseModel):
    id: int
    code: str
