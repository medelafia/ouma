from models.models import Anomaly
from sqlmodel import Session , select
from db.mysql_db_connection import get_engine 
from uuid import uuid4
from datetime import datetime 


def create_and_save_anomaly(instance) : 
    uuid = uuid4() 
    anomaly_date = datetime.now().date() 
    anomaly_time = datetime.now().time() 
    anomaly = Anomaly(anomaly_id=uuid , detection_time=anomaly_time , detection_date=anomaly_date ,duration=0 , instance=instance)
    with Session(get_engine()) as session : 
        session.add(anomaly) 
        session.commit()
    
    return anomaly



def get_all_anomalies(limit) : 
    with Session(get_engine() ) as session : 
        return session.exec(select(Anomaly).offset(0).limit(limit)).all() 

def get_anomalies_by_instance_id(instance_id) : 
    with Session(get_engine()) as session : 
        return session.exec(select(Anomaly).where(Anomaly.instance_id == instance_id)).all()