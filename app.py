

"""
    Copy Right 2026 (C) Mohamed EL AFIA                             
    Tool Name : Ouma  
    Purpose : Cycle End Project                               
"""

from fastapi import FastAPI 
from core.prometheus_module import fetch_metrics  ,  fetch_instances 
import json 
import datetime


services = [] 

app = FastAPI()

@app.get("/kpis")
def get_kpis() :
    return 

@app.get("/instances/all") 
def get_all_services() : 
    try :
        instances = fetch_instances()
    
        return instances
    except Exception as ex:
        error_response = {
            "details" :  str(ex) , 
            "timestamp" : datetime.datetime.now(), 
            "status_code" : 500 
        } 
        return error_response

@app.get("/services/metrics") 
def get_service_metrics() : 
    return fetch_metrics()

@app.get("/services/<service_name>/anomalies")
def get_service_anomalies(service_name : str) : 
    return ""



