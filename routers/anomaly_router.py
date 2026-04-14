from fastapi import APIRouter 
from services.anomaly_service import get_all_anomalies , get_anomalies_by_instance_id


anomaly_router = APIRouter(prefix="/api/v1/anomalies")



@anomaly_router.get("/all") 
def get_all_anomalies_route() : 
    return get_all_anomalies()  


@anomaly_router.get("/{instance_id}/all") 
def get_anomalies_by_instance_id_route(instance_id) : 
    return get_anomalies_by_instance_id(instance_id) 