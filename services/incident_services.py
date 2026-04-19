from sqlmodel import Session  , select , func
from db.mysql_db_connection import get_engine
from models.models import Incident

def get_all_incidents(limit : int= 10) : 
    with Session(get_engine() ) as session : 
        return session.exec(select(Incident).offset(0).limit(10)).all()
    


def get_incidents_count() :
    with Session(get_engine() ) as session : 
        return { "count" : session.exec(select(func.count()).select_from(Incident)).one() } 
    
def save_incident() : 
    pass 