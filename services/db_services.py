from db.mysql_db_connection import get_mysql_connection
from uuid import uuid4
from typing import Annotated
from fastapi import Depends 
from sqlmodel import Session
from db.mysql_db_connection import get_session

SessionDep = Annotated[Session, Depends(get_session)]




def savePrediction() : 
    pass