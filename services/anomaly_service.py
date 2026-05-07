from models.models import Anomaly
from sqlmodel import Session , select , func , text
from db.mysql_db_connection import get_engine 
from uuid import uuid4
from datetime import datetime 
from schemas.schemas import PageMetadata , Page
from math import ceil 


def create_and_save_anomaly(instance) : 
    uuid = uuid4() 
    anomaly_date = datetime.now().date() 
    anomaly_time = datetime.now().time() 
    anomaly = Anomaly(anomaly_id=uuid , detection_time=anomaly_time , detection_date=anomaly_date ,duration=0 , instance=instance)
    with Session(get_engine()) as session : 
        session.add(anomaly) 
        session.commit()
        session.refresh(anomaly)
    
        return anomaly


def save_anomaly(anomaly) : 
    with Session(get_engine()) as session : 
        session.add(anomaly) 
        session.commit()
        session.refresh(anomaly)
        return anomaly


def get_all_anomalies(page , size , from_date, to  ) : 
    with Session(get_engine() ) as session : 
        result = session.exec(select(Anomaly).where((Anomaly.detection_date >= from_date) & (Anomaly.detection_date <= to )).offset(page * size).limit(size)).all()
        total_pages =  ceil(session.exec(select(func.count()).select_from(Anomaly).where((Anomaly.detection_date >= from_date) & (Anomaly.detection_date <= to ))).one() / size )

        return Page(content=result , metadata=PageMetadata(page=page, size=size , totalPages=total_pages))
def get_anomalies_by_instance_id(instance_id) : 
    with Session(get_engine()) as session : 
        return session.exec(select(Anomaly).where(Anomaly.instance_id == instance_id)).all()


def get_anomalies_count() : 
    with Session(get_engine()) as session : 
        return { "count" : session.exec(select(func.count()).select_from(Anomaly)).one() } 

