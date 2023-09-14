from pydantic import BaseModel
from typing import Union, List


class MaterialBase(BaseModel):
    id: int | None = None
    material_name: str
    material_lot: str
    material_EOV: str


class EquipmentsBase(BaseModel):
    id: int | None = None
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


class delBae(BaseModel):
    del_id: int
