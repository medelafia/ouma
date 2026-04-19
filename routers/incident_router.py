from fastapi import APIRouter 
from services.incident_services import get_all_incidents, get_incidents_count


incident_router = APIRouter(prefix="/api/v1/incidents")



@incident_router.get("/all")
def get_all_incidents_route(limit : int ) :
    return get_all_incidents(limit) 


@incident_router.get("/all/count")
def get_incidents_count_route( ) : 
    return get_incidents_count( )