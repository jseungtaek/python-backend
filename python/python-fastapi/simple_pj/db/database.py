from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

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

Session = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=ENGINE
)

Base = declarative_base()