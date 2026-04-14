from fastapi import APIRouter 
from services.alerting_services import send_alert, get_alerts


alerts_router = APIRouter(prefix="/api/v1/alerts")


@alerts_router.get("/all") 
def get_all_alerts() : 
    return get_alerts(10)
