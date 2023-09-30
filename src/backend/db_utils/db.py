from sqlalchemy import URL, Engine, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE = {
    "drivername": "postgresql",
    "host": "127.0.0.1",
    "port": "5433",
    "username": os.getenv("POSTGRES_USER"),
    "password": os.getenv("POSTGRES_PASSWORD"),
    "database": "my_database",
}




#engine = create_engine(DATABASE_URL)
#Session = sessionmaker(bind=engine)
#Base = declarative_base()
#Base.metadata.create_all(engine)

Base = declarative_base()


def db_connect() -> Engine:

    return create_engine(URL.create(**DATABASE))

def create_albums_table(engine: Engine):

    Base.metadata.create_all(engine)

def get_session(autocommit=True, autoflush=True):

    engine = db_connect()
    Session = sessionmaker(autocommit=autocommit, autoflush=autoflush, bind=engine)
    return Session()