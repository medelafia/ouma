from pydantic import BaseModel  , EmailStr , Field
from typing import Optional 
from datetime import date , time ,datetime


 
##################### Prediction Engine related schemas #####################


class Prediction(BaseModel ) : 
    timestamp: datetime 
    anomaly_score: float = Field(default=0)
    instance_id : str 



class MetricsPrediction(Prediction) :
    cpu_usage : float
    memory_usage : float


class Instance(BaseModel) : 
    instance_id: str 
    port : int 
    ip_address : str


class Amomaly(BaseModel) :
    anomaly_id : str 
    detection_time : time
    detection_date : date 
    duration : int 

class Alert(BaseModel) :
    alert_id : str 
    send_time : time 
    send_date :date 
    status : str
    content: str 


class Incident(BaseModel) :
    incident_id : str 
    incident_time : time 
    incident_date : date
    description : str 





##################### AUTH RELATED Schemas #####################

class User(BaseModel) : 
    username : str = Field(None ,description="Usernae is required") 
    password : str = Field(None , description="Password is required , please entert a valid password")
    email: EmailStr



class Metadata(BaseModel) : 
    TARGET_SERVER_HOST : str | None = Field(None ) 
    TARGET_SERVER_PORT: int | None = Field(None ) 
    PREDICTION_INTERVAL : int | None = Field(None) 
    ACTIVATE_ALERTING : bool | None = Field(None )