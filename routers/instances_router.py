from fastapi import APIRouter , Depends , HTTPException
from services.prometheus_service import fetch_metrics  , fetch_instance_metrics, fetch_instance_ressources 
import datetime 
from services.influx_service import load_metrics , load_all_metrics, delete_all_metrics_by_instance_id
from utils.instance_factory import get_instances , get_instance_by_id 
from auth.auth import get_current_user



instances_routers = APIRouter(prefix="/api/v1/instances")

@instances_routers.get("/all") 
def get_all_services(token : str = Depends(get_current_user)) : 
    try :
        instances = get_instances()

        for instance in instances : 
            instance.cpu_usage , instance.memory_usage = fetch_instance_ressources(instance) 
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
    start_time = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(hours=5 )

    return load_metrics(instance_id, start_time , measurment="predicted_measurement")

@instances_routers.get("/{instance_id}/metrics/real" )
def get_reals_metrics(instance_id ,token : str = Depends(get_current_user)):
    start_time = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(hours=5 )

    return load_metrics(instance_id, start_time , measurment="real_measurement")

@instances_routers.get("/{instance_id}/metrics/all" )
def get_reals_metrics(instance_id , from_date : str ,token : str = Depends(get_current_user)): 
    start_datetime = datetime.datetime.fromisoformat(from_date[:-1]).replace(tzinfo=datetime.timezone.utc)
    return load_all_metrics(instance_id, start_datetime )


@instances_routers.delete("/{instance_id}/metrics/all")
def delete_metrics_route(instance_id : str , token : str = Depends(get_current_user) ) : 
    try : 
        return delete_all_metrics_by_instance_id(instance_id)
    except Exception as ex:    
        print(ex)
        exception = HTTPException(
            status_code=500,
            detail=f"cannot delete history"
        )
        return exception
