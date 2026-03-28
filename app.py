from fastapi import FastAPI 
from core.prometheus_module import fetch_metrics  ,  fetch_nodes
import json 
import datetime
services = [] 

app = FastAPI()

@app.get("/kpis")
def get_kpis() :
    return 

@app.get("/services/all") 
def get_all_services() : 
    try :
        services = fetch_nodes()
    
        return services
    except Exception as ex:
        error_response = {
            "details" :  str(ex) , 
            "timestamp" : datetime.datetime.now(), 
            "status_code" : 500 
        } 
        return error_response

@app.get("/services/<service_name>/metrics") 
def get_service_metrics(service_name : str) : 
    return 

@app.get("/services/<service_name>/anomalies")
def get_service_anomalies(service_name : str) : 
    return ""



