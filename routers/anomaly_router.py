from fastapi import APIRouter  , Depends
from services.anomaly_service import get_all_anomalies , get_anomalies_by_instance_id , create_and_save_anomaly , get_anomalies_count
from auth.auth import  get_current_user

anomaly_router = APIRouter(prefix="/api/v1/anomalies")


@anomaly_router.get("/all") 
def get_all_anomalies_route(token : str = Depends(get_current_user)) : 
    return get_all_anomalies(10)  


@anomaly_router.get("/{instance_id}/all") 
def get_anomalies_by_instance_id_route(instance_id, token : str = Depends(get_current_user)) : 
    return get_anomalies_by_instance_id(instance_id) 

@anomaly_router.get("/all/count")
def get_anomalies_count_route(token : str = Depends(get_current_user)) : 
    return get_anomalies_count()