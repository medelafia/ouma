from models.models import Anomaly
from sqlmodel import Session
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
