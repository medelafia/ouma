from fastapi import APIRouter 
from services.metadata_services import update_metadata , get_metadata
from schemas.schemas import Metadata


metadata_router = APIRouter(prefix="/api/v1/metadata") 

@metadata_router.post("/update")
def update_metadata_router(metadata : Metadata) : 
    return update_metadata(metadata)

@metadata_router.get("/")
def get_metadata_router() : 
    return get_metadata()