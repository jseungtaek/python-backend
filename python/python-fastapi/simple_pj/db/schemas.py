from typing import Union
from pydantic import BaseModel
from jose import JWTError, jwt


class Key:
    SECRET_KEY = "685d92303dd86f5338a97893d39b9138cfd1fbb95a46d6cf916f292f8b13563b"
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30


class UserBase(BaseModel):
    id: int
    username: str
    password: str

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None


class UserInDB(UserBase):
    password: str


class UserInfo(BaseModel):
    username: str
