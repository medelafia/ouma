from fastapi import APIRouter , Depends
from services.incident_services import get_all_incidents, get_incidents_count
from auth.auth import get_current_user

incident_router = APIRouter(prefix="/api/v1/incidents")



@incident_router.get("/all")
def get_all_incidents_route(limit : int , token : str = Depends(get_current_user)) :
    return get_all_incidents(limit) 


@incident_router.get("/all/count")
def get_incidents_count_route(token : str = Depends(get_current_user)) : 
    return get_incidents_count( )