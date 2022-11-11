from curses.ascii import HT
from email.policy import HTTP
from datetime import datetime, timedelta
from typing import List, Union
from fastapi import Depends, FastAPI, HTTPException, status, Header
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from jose import JWTError, jwt

import uvicorn
import json
import jsonpickle

from db import crud
from db import schemas
from db import models
from db.database import Session, ENGINE

models.Base.metadata.create_all(bind=ENGINE)

app = FastAPI()


def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()


@app.get("/users/", response_model=list[schemas.UserBase])
def read_user(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{id}", response_model=schemas.UserBase)
def read_user(id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="not found")
    return db_user


@app.get("/users/checks/{username, password}", response_model=schemas.UserBase)
def check_user(username: str, password: str, db: Session = Depends(get_db)):
    db_us = crud.authenticate_user(db, username, password)
    return db_us


@app.post("/users/{username, password}", response_model=schemas.UserBase)
def create_user(username: str, password: str, db: Session = Depends(get_db)):
    db_user = crud.get_us_username(db, username)
    if db_user:
        raise HTTPException(status_code=404, detail="already registered")
    return crud.create_user(db, username, password)


# async def get_current_user(token: str = Depends(crud.oauth2_scheme)):
#     payload = jwt.decode(token, schemas.Key.SECRET_KEY, schemas.Key.ALGORITHM)
#     username: str = payload.get("sub")
#     token_data = schemas.TokenData(username=username)
#     user = crud.get_user_token(Depends(get_db), username=token_data.username)
#     return user


async def get_current_user(token: str = Depends(crud.oauth2_scheme), db: Session = Depends(get_db)):
    credential_exception = HTTPException(
        # status_code=status.HTTP_401_UNAUTHORIZED,
        # detail="Could not validate credentials",
        # headers={"WWW-Authenticate": "Bearer"},
        status_code=401
    )
    try:
        payload = jwt.decode(token, schemas.Key.SECRET_KEY, schemas.Key.ALGORITHM)
        username: str = payload.get("sub")
        if username is None:
            raise credential_exception
        token_data = schemas.TokenData(username=username)
    except JWTError:
        raise credential_exception
    user = crud.get_us_username(db, username)
    user = jsonpickle.encode(user)
    if user is None:
        raise credential_exception
    return user


async def get_current_active_user(current_user: schemas.UserBase = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@app.post("/token", response_model=schemas.Token)
async def check_user(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=schemas.Key.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = crud.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    # users = crud.get_us_username(db, form_data.username)
    # print(users)
    # print(type(users))
    # asdf = jsonpickle.encode(users)
    # print(asdf)
    # print(type(asdf))
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/check/me", response_model=schemas.UserBase)
async def read_users_me(current_user: schemas.UserBase = Depends(get_current_active_user)):
    return current_user


# @app.get("/users/test", response_model=schemas.UserInfo)
# async def test(token: str = Depends(crud.oauth2_scheme), db: Session = Depends(get_db)):
#     payload = jwt.decode(token, schemas.Key.SECRET_KEY, schemas.Key.ALGORITHM)
#     username: str = payload.get("sub")
#     token_data = schemas.TokenData(username=username)
#     user = crud.get_user_token(db, username=token_data.username)
#     users = crud.get_us_username(db, token_data.username)
#     return users





