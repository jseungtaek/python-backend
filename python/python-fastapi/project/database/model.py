from sqlalchemy import Column, Integer, String
from pydantic import BaseModel
from schema import Base
from schema import ENGINE

class UserTable(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    age = Column(Integer)

class User(BaseModel):
    id___:int
    name_:str
    age__:int