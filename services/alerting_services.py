from models.models import Alert
from db.mysql_db_connection import create_db_and_tables , get_engine
from uuid import uuid4 
from datetime import  datetime
from sqlmodel import Session , select

create_db_and_tables()

def send_alert() : 
    with Session(get_engine()) as session : 
        alert = Alert(alert_id=uuid4() ,send_date=datetime.now().date() , send_time=datetime.now().time()  , status="UNSEEN" ,content="High cpu usage after 5min")

        session.add(alert)
        session.commit()

def get_alerts(limit) : 
    with Session(get_engine()) as session :
        return session.exec(select(Alert).offset(0).limit(limit)).all()


def get_incident_alert():
    pass 

