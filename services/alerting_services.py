from models.models import Alert
from db.mysql_db_connection import create_db_and_tables , get_engine
from uuid import uuid4 
from datetime import  datetime
from sqlmodel import Session , select , func , text 
from services.email_services import load_emails
from schemas.schemas import Page , PageMetadata
from math import ceil
from services.email_services import notify_admins_by_emails


def send_alert(content , severity , anomaly_id) : 
    send_date = datetime.now().date() 
    send_time = datetime.now().time() 
    uuid = uuid4()
    print("sending alert ...")
    with Session(get_engine()) as session : 
        alert = Alert(alert_id=uuid ,send_date=send_date , send_time=send_time  , status="UNSEEN" ,content=content , severity=severity , anomaly_id=anomaly_id)
        session.add(alert)
        session.commit()
        email_content = f"""
            🚨 ALERT NOTIFICATION

            Details:
            • Message: {alert.content}

            • Occurrence Time: {str(alert.send_date) + " " + str(alert.send_time)}

            • Related Anomaly ID: {alert.anomaly_id}

            Please review this alert as soon as possible and take the necessary action.
        """
        notify_admins_by_emails('System Alert!', email_content)
        



def get_all_alerts(page , size , from_date, to  ) : 
    with Session(get_engine() ) as session : 
        result = session.exec(select(Alert).where((Alert.send_date >= from_date) & (Alert.send_date <= to )).offset(page * size).limit(size)).all()
        total_pages = ceil(session.exec(select(func.count()).select_from(Alert).where((Alert.send_date >= from_date) & (Alert.send_date <= to ))).one() / size)

        return Page(content=result , metadata=PageMetadata(page=page, size=size , totalPages=total_pages))


def get_alert_by_anomaly(anomaly_id):
    with Session(get_engine()) as session :
        return session.exec(select(Alert).where(Alert.anomaly_id == anomaly_id)).all()    



def get_alerts_count() : 
    with Session(get_engine()) as session : 
        return { "count" :  session.exec(select(func.count()).select_from(Alert)).one() } 


def get_overview(start_date) : 
    with Session(get_engine() ) as session : 
        query = f"""
            WITH 
            alerts AS (
                SELECT send_date AS date, COUNT(*) AS cnt 
                FROM alert 
                WHERE send_date > {start_date}
                GROUP BY send_date 
            ),
            incidents AS (
                SELECT incident_date AS date, COUNT(*) AS cnt 
                FROM incident 
                WHERE incident_date > {start_date}
                GROUP BY incident_date 
            ), 
            anomalies AS (
                SELECT detection_date AS date, COUNT(*) AS cnt 
                FROM anomaly 
                WHERE detection_date > {start_date}
                GROUP BY detection_date 
            )
            SELECT 
                COALESCE(i.date, a.date, an.date) AS date,
                COALESCE(i.cnt, 0) AS incidents_count,
                COALESCE(a.cnt, 0) AS alerts_count,
                COALESCE(an.cnt, 0) AS anomalies_count
            FROM incidents i
            LEFT JOIN alerts a ON i.date = a.date
            LEFT JOIN anomalies an ON i.date = an.date

            UNION

            SELECT 
                COALESCE(a.date, an.date) AS date,
                0,
                COALESCE(a.cnt, 0),
                COALESCE(an.cnt, 0)
            FROM alerts a
            LEFT JOIN anomalies an ON a.date = an.date
            LEFT JOIN incidents i ON a.date = i.date
            WHERE i.date IS NULL

            UNION

            SELECT 
                an.date,
                0,
                0,
                an.cnt
            FROM anomalies an
            LEFT JOIN incidents i ON an.date = i.date
            LEFT JOIN alerts a ON an.date = a.date
            WHERE i.date IS NULL AND a.date IS NULL

            ORDER BY date;
        """
        result = session.exec(text(query)).all()
        print(result)
        return [ { "date" : str(row[0]) , "incidents_count" : row[1] , "alerts_count" : row[2] , "anomalies_count" : row[3]}for row in result ] 




