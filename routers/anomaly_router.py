from fastapi import APIRouter 
from services.anomaly_service import get_all_anomalies , get_anomalies_by_instance_id , create_and_save_anomaly , get_anomalies_count


anomaly_router = APIRouter(prefix="/api/v1/anomalies")
create_and_save_anomaly("1sksjksknsksksknnkss")




@anomaly_router.get("/all") 
def get_all_anomalies_route() : 
    return get_all_anomalies(10)  


@anomaly_router.get("/{instance_id}/all") 
def get_anomalies_by_instance_id_route(instance_id) : 
    return get_anomalies_by_instance_id(instance_id) 

@anomaly_router.get("/all/count")
def get_anomalies_count_route() : 
    return get_anomalies_count()