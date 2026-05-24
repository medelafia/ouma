from fastapi import APIRouter , Depends
from services.incident_services import get_all_incidents, get_incidents_count , save_incident, delete_incident_by_id
from auth.auth import get_current_user
from schemas.schemas import Incident

from datetime import datetime 
incident_router = APIRouter(prefix="/api/v1/incidents")


@incident_router.get("/all")
def get_all_incidents_route(from_date : str , to : str , token : str = Depends(get_current_user) , size : int = 10  , page : int = 0) :
    return get_all_incidents(page , size, datetime.fromisoformat(from_date[:-1]).date() , datetime.fromisoformat(to[:-1]).date()) 

@incident_router.get("/all/count")
def get_incidents_count_route(token : str = Depends(get_current_user)) : 
    return get_incidents_count( )

@incident_router.post("/")
def save_incident_route(incident : Incident , token : str = Depends(get_current_user)) : 
    return save_incident(incident)

@incident_router.delete("/{id}")
def delete_incident(id : str) :
    return delete_incident_by_id(id)