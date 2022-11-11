from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
import os
from dotenv import load_dotenv


load_dotenv()

user_name = os.environ['user_name']
user_pwd = os.environ['user_pwd']
db_host = os.environ['db_host']
db_name = os.environ['db_name']

DATABASE = 'mysql://%s:%s@%s/%s?charset=utf8' % (
    user_name,
    user_pwd,
    db_host,
    db_name
)

ENGINE = create_engine(
    DATABASE,
    encoding="utf-8",
    echo=True
)

session = scoped_session(
    sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=ENGINE
    )
)

Base = declarative_base()
Base.query = session.query_property()