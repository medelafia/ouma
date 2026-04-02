from fastapi import APIRouter 
from core.prometheus_module import fetch_metrics  ,  fetch_instances 
import datetime 




instances_routers = APIRouter(prefix="/api/v1/instances")

@instances_routers.get("/all") 
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

@instances_routers.get("/instances/metrics") 
def get_service_metrics() : 
    return fetch_metrics()

