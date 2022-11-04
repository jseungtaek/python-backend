from curses.ascii import HT
from email.policy import HTTP
from typing import List
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from db import crud
from db import schemas
from db import models
from db import database #Session, ENGINE


models.database.Base.metadata.create_all(bind=database.ENGINE)

app = FastAPI()

def get_db():
    db = database.Session()
    try:
        yield db
    finally:
        db.close()


@app.get("/users/", response_model=list[schemas.UserBase])
def read_user(skip: int = 0, limit: int = 100, db: database.Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

@app.get("/users/{id}", response_model=schemas.UserBase)
def read_user(id: int, db:database.Session = Depends(get_db)):
    db_user = crud.get_user(db, id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="not found")
    return db_user

@app.post("/users/{email, pw}", response_model=schemas.UserBase)
def create_user(email: str, pw: str, db: database.Session = Depends(get_db)):
    db_user = crud.get_us_email(db, email)
    if db_user:
        raise HTTPException(status_code=404, detail="already registered")
    return crud.create_user(db, email, pw)

