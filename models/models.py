from pydantic import BaseModel  , EmailStr , Field
from typing import Optional 
import datetime 




"""
    Prediction Engine related schemas 
"""

class Prediction(BaseModel ) : 
    timestamp: datetime 
    anomaly_score: float 
    cpu_usage : float
    memory_usage : float


class Alert(BaseModel) :
    pass 




class Microservie(BaseModel) :
    pass

class Instance(BaseModel) : 
    instanceId: str 
    port : int 
    ipAddress : str


class PredictedMetrics(BaseModel):
    pass 

class Amomaly(BaseModel) :
    pass 

class Incident(BaseModel) :
    pass





"""

    Auth related schemas

"""

class User(BaseModel) : 
    username : str = Field(None ,description="Usernae is required") 
    password : str = Field(None , description="Password is required , please entert a valid password")
    email: EmailStr

