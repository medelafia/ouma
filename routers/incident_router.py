from fastapi import APIRouter 
from services.alerting_services import send_alert, get_alerts


incident_router = APIRouter(prefix="/api/v1/incidents")



@incident_router.get("/all")
def get_all_incidents() :
    return []
