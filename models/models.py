from sqlmodel import Field, Session, SQLModel, create_engine, select
from datetime import time , date , datetime 

class Instance(SQLModel, table=True):
    instance_id : str | None = Field(default=None, primary_key=True)
    ip_address : str = Field(index=True)
    port : int | None = Field(default=None, index=True)

class Alert(SQLModel , table=True) : 
    alert_id : str | None = Field(default=None , primary_key = True )
    send_time : time = Field(default=datetime.now().time() )
    send_date: date = Field(default=datetime.now().date() ) 
    status : str = Field(default="UNSEEN") 
    content : str | None = Field(default=None ) 
    severity : str | None = Field(None)
    anomaly_id : str | None = Field(default=None , foreign_key="anomaly.anomaly_id")

class Anomaly(SQLModel , table=True) : 
    anomaly_id : str | None = Field(default=None ,primary_key= True ) 
    detection_time : time = Field(default=datetime.now().time() )
    detection_date: date = Field(default=datetime.now().date() ) 
    duration : int = Field(default=0 , description="How many seconds anomaly detected")

    instance_id : str | None = Field(default=None , foreign_key="instance.instance_id")

class Incident(SQLModel , table=True ) : 
    incident_id : str | None = Field(default=None , primary_key=True)
    incident_time : time = Field(default=datetime.now().time() )
    incident_date : date = Field(default=datetime.now().date() ) 
    description : str | None = Field(default=None)

    alert : str | None = Field(default=None , foreign_key="alert.alert_id")