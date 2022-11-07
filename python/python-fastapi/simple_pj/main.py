from curses.ascii import HT
from email.policy import HTTP
from datetime import datetime, timedelta
from typing import List
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from jose import JWTError, jwt

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


@app.post("/users/check/{username}", response_model=schemas.UserBase)
def check_user(username: str, db: Session = Depends(get_db)):
    check_us = crud.get_user_check(db, username)
    # check_us = crud.authenticate_user(db, username, password)
    return check_us


@app.post("/token", response_model=schemas.Token)
async def check_user(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED
        )
    access_token_expires = timedelta(minutes=schemas.Key.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = crud.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


async def get_current_user(token: str = Depends(crud.oauth2_scheme), db: Session = Depends(get_db)):
    credential_exception = HTTPException(
        status_code=401
    )
    try:
        payload = jwt.decode(token, schemas.Key.SECRET_KEY, schemas.Key.ALGORITHM)
        username: str = payload.get("sub")
        if username is None:
            raise credential_exception
        token_data = schemas.ToKenData(username=username)
    except JWTError:
        raise credential_exception
    user = crud.get_user(db, username=token_data.username)
    if user is None:
        raise credential_exception
    return user


async def get_current_active_user(current_user: schemas.UserBase = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@app.get("/users/me", response_model=schemas.UserBase)
async def read_users_me(current_user: schemas.UserBase = Depends(get_current_active_user)):
    return current_user
