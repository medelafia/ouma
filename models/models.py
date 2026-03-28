from pydantic import BaseModel  , EmailStr , Field
from typing import Optional 
import datetime 




"""
    Prediction Engine related schemas 
"""

class Prediction(BaseModel ) : 
    timestamp: datetime 
    anomaly_score: float 


class Alert(BaseModel) :
    pass 



class Node(BaseModel) : 
    pass

class Microservie(BaseModel) :
    pass

class Insrance(BaseModel) : 
    pass 

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

