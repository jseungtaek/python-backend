from typing import Union
from pydantic import BaseModel

class UserBase(BaseModel):
    id:int
    email:str
    pw:str

    class Config:
        orm_mode = True
