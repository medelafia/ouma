from fastapi import APIRouter , Depends 
from services.prometheus_service import fetch_metrics  , fetch_instance_metrics
import datetime 
from services.influx_service import load_metrics
from utils.instance_factory import get_instances , get_instance_by_id 
from auth.auth import get_current_user
instances_routers = APIRouter(prefix="/api/v1/instances")

@instances_routers.get("/all") 
def get_all_services(token : str = Depends(get_current_user)) : 
    try :
        instances = get_instances()
    
        return instances
    except Exception as ex:
        error_response = {
            "details" :  str(ex) , 
            "timestamp" : datetime.datetime.now(), 
            "status_code" : 500 
        } 
        return error_response



@instances_routers.get("/all/count") 
def get_instances_count(token : str = Depends(get_current_user)):
    return { "count" : len(get_instances()) } 

@instances_routers.get("/metrics") 
def get_services_metrics() : 
    return fetch_metrics()

@instances_routers.get("/{instance_id}/metrics")
def get_service_metrics(instance_id , token : str = Depends(get_current_user)): 
    instance = get_instance_by_id(instance_id)
    if not instance is None :
        instance_host = instance.ip_address + ":" + str(instance.port)
        return fetch_instance_metrics(instance_host)
    return {}

@instances_routers.get("/{instance_id}/metrics/predicted")
def get_predicted_metrics(instance_id , token : str = Depends(get_current_user)) : 
    ## to query by date in influxdb , the date should be in utc format
    start_time = (datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(hours=5 )).isoformat().split(".")[0] + "Z"
    return load_metrics(instance_id, start_time , measurment="predicted_measurement")

@instances_routers.get("/{instance_id}/metrics/reals" )
def get_reals_metrics(instance_id ,token : str = Depends(get_current_user)) : 
    start_time = (datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(hours=5 )).isoformat().split(".")[0] + "Z"
    return load_metrics(instance_id, start_time , measurment="real_measurement")


