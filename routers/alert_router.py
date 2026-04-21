from fastapi import APIRouter , Depends
from services.alerting_services import send_alert, get_alerts
from auth.auth import get_current_user

alerts_router = APIRouter(prefix="/api/v1/alerts")


@alerts_router.get("/all") 
def get_all_alerts(token : str = Depends(get_current_user)) : 
    return get_alerts(10)
