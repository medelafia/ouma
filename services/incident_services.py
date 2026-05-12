from sqlmodel import Session  , select , func , text
from db.mysql_db_connection import get_engine
from models.models import Incident
from datetime import date 
from schemas import schemas
from math import ceil 
from models import models 
from uuid import uuid4


def get_all_incidents(page , size , from_date, to  ) : 
    with Session(get_engine() ) as session : 
        result = session.exec(select(Incident).where((Incident.incident_date >= from_date) & (Incident.incident_date <= to )).offset(page * size).limit(size)).all()
        total_pages = ceil(session.exec(select(func.count()).select_from(Incident).where((Incident.incident_date >= from_date) & (Incident.incident_date <= to ))).one() / size )

        return schemas.Page(content=result , metadata=schemas.PageMetadata(page=page, size=size , totalPages=total_pages))
def get_incidents_count() :
    with Session(get_engine() ) as session : 
        return { "count" : session.exec(select(func.count()).select_from(Incident)).one() } 
    
def save_incident(incident : Incident ) : 
    with Session(get_engine() ) as session : 
        incident_to_insert = models.Incident(incident_id=str(uuid4()) , incident_date=incident.incident_date , incident_time=incident.incident_time , description=incident.description , alert=incident.alert_id)
        session.add(incident_to_insert)
        session.commit()
        return incident_to_insert
