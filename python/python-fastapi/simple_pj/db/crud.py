from sqlalchemy.orm import session
import bcrypt
from fastapi import Depends, HTTPException
from typing import Union
from datetime import datetime, timedelta
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer

#절대경로 설정
# import sys, os
# sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from . import models
from . import schemas


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_user(db:session, id: int):
    return db.query(models.User).filter(models.User.id==id).first()

def get_us_username(db:session, username: str):
    return db.query(models.User).filter(models.User.username==username).first()

def get_users(db:session, skip:int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


# def get_user_check(db: session, username:str):
#     # if username in db:
#     #     user_dict = db[username]
#     #     return schemas.UserInDB(**user_dict)

def create_user(db: session, username: str, password: str):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt) #[:50]
    db_user = models.User(username = username, password = hashed)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def verify_password(plain_password, hashed_password):
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password)

def authenticate_user(db: session, username: str, password: str):
    user = get_us_username(db, username)
    print(1)
    if not user:
        print(2)
        return False
    print(3)
    if not verify_password(password, user.password):
        print(4)
        return False
    print(5)
    return user

def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, schemas.Key.SECRET_KEY, schemas.Key.ALGORITHM)
    return encoded_jwt

