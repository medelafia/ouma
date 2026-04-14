from models.models import Alert
from db.mysql_db_connection import create_db_and_tables , get_engine
from uuid import uuid4 
from datetime import  datetime
from sqlmodel import Session , select

create_db_and_tables()

def send_alert(content , severity , anomaly_id) : 
    send_date = datetime.now().date() 
    send_time = datetime.now().time() 
    uuid = uuid4()

    print("sending alert")
    with Session(get_engine()) as session : 
        alert = Alert(alert_id=uuid ,send_date=send_date , send_time=send_time  , status="UNSEEN" ,content=content , severity=severity , anomaly_id=anomaly_id)

        session.add(alert)
        session.commit()

def get_alerts(limit) : 
    with Session(get_engine()) as session :
        return session.exec(select(Alert).offset(0).limit(limit)).all()


def get_incident_alert():
    pass 