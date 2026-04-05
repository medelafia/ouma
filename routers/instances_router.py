from fastapi import APIRouter 
from services.prometheus_service import fetch_metrics  ,  fetch_instances 
import datetime 
from services.ressource_prediction_services import prepare_data_input

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

@instances_routers.get("/metrics") 
def get_services_metrics() : 
    return fetch_metrics()

@instances_routers.get("/metrics/prepared") 
def get_services_metrics() : 
    return prepare_data_input()



@instances_routers.get("/<instance_id>/metrics")
def get_service_metrics(): 
    
    return 

