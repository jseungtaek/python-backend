from fastapi import FastAPI
from typing import List
from starlette.middleware.cors import CORSMiddleware

from schema import session
from model import UserTable, User

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/users")
def read_users():
    users = session.query(UserTable).all()
    return users

@app.get("/users/{user_id}")
def read_users():
    users = session.query(UserTable).filter(UserTable.id == user_id).first()
    return users

@app.get("/users")
def create_users(name: str, age: int):
    
    user = UserTable()
    user.name = name
    user.age = age
    
    session.add(user)
    session.commit()

    return f"{name} create..."

@app.put("/users")
def update_users(users: List[User]):

    for i in users:
        user = session.query(UserTable).filter(UserTable.id == i.id).first()
        user.name = i.name
        user.age = i.age
        session.commit()

    return f"{users[0].name} update..."

@app.delete("/users")
def delete_users(user_id: int):
    user = session.query(UserTable).filter(UserTable.id == user_id).delete()
    session.commit()
    return read_users