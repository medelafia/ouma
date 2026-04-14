from fastapi import APIRouter 
from services.alerting_services import send_alert, get_alerts


anomaly_router = APIRouter(prefix="/api/v1/anomalies")



@anomaly_router.get("/all") 
def get_all_anomalies() : 
    pass 


@anomaly_router.get("/{instance_id}/all") 
def get_anomalies_by_instance_id() : 
    pass 