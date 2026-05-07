from fastapi import APIRouter , Depends
from services.alerting_services import get_all_alerts
from auth.auth import get_current_user
from datetime import datetime 
alerts_router = APIRouter(prefix="/api/v1/alerts")


@alerts_router.get("/all") 
def get_all_alerts_router(from_date : str , to : str , token : str = Depends(get_current_user) , size : int = 10  , page : int = 0) : 
    return get_all_alerts(page , size , datetime.fromisoformat(from_date[:-1]).date() , datetime.fromisoformat(to[:-1]).date() )
