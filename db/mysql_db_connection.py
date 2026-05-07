from utils.env_factory import get_config
from sqlmodel import SQLModel, create_engine

MYSQL_USER = get_config("MYSQL_USER")
MYSQL_PASSWORD = get_config("MYSQL_PASSWORD")
MYSQL_DB = get_config("MYSQL_DB")
MYSQL_HOST = get_config("MYSQL_HOST")

mysql_url = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DB}?charset=utf8mb4"

connect_args = {"check_same_thread": False}
engine = None


def create_db_and_tables():
    SQLModel.metadata.create_all(get_engine() )


def get_engine() : 
    global engine
    if engine == None : 
        engine = create_engine(mysql_url )

    return engine