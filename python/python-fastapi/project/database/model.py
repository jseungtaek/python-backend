import email
from sqlalchemy import Column, Integer, String
from pydantic import BaseModel
from schema import Base
from schema import ENGINE

class UserTable(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(50), nullable=False)
    pw = Column(String(50))

class User(BaseModel):
    id:int
    email:str
    pw:str