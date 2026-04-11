from fastapi import APIRouter 
from services.prometheus_service import fetch_metrics  ,  fetch_instances 
import datetime 
from services.ressource_prediction_services import prepare_data_input
from services.influx_service import save_actual_records , load_metrics



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
    prepare_data_input()
    return fetch_metrics()

@instances_routers.get("/{instance_id}/metrics")
def get_service_metrics(): 
    
    return 



@instances_routers.get("/")
def save() : 
    save_actual_records("ndkdnkndkk" , 10 , 137 , 1197919199)
    return "saved"



@instances_routers.get("/{instance_id}/metrics/predicted")
def get_predicted_metrics(instance_id) : 
    ## to query by date in influxdb , the date should be in utc format
    start_time = (datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(hours=5 )).isoformat().split(".")[0] + "Z"
    return load_metrics("http://localhost:9091", start_time , measurment="predicted_measurement")



@instances_routers.get("/{instance_id}/metrics/reals")
def get_reals_metrics(instance_id) : 
    start_time = (datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(hours=5 )).isoformat().split(".")[0] + "Z"
    return load_metrics("http://localhost:9091", start_time , measurment="real_measurement")
