from cgi import print_arguments
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

# import sys, os
# sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from .database import Base


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(80), nullable=False)
    password = Column(String(80))

    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    # def __str__(self, username: str, password: str):
    #     return self.username + self.password
