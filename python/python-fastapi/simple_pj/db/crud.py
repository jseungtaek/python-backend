from sqlalchemy.orm import session
import bcrypt
from . import models, schemas

def get_user(db:session, id: int):
    return db.query(models.User).filter(models.User.id==id).first()

def get_us_email(db:session, email: str):
    return db.query(models.User).filter(models.User.email==email).first()

def get_users(db:session, skip:int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: session, email: str, pw: str):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(pw.encode('utf-8'), salt)[:50]
    db_user = models.User(email = email, pw = hashed)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user