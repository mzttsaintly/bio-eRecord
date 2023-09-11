from pydantic import BaseModel
from typing import Union


class MaterialBase(BaseModel):
    material_id: int | None = None
    material_name: str
    material_lot: str
    material_EOV: str


class EquipmentsBase(BaseModel):
    equipments_id: int | None = None
    equipName: str
    equipNum: str
    place: str


class UserBase(BaseModel):
    user_name: str
    authority: int


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None
