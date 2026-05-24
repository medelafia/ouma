from fastapi import APIRouter , Depends
from services.metadata_services import update_metadata , get_metadata 
from services.email_services import add_new_email , delete_email , load_emails
from schemas.schemas import Metadata
from auth.auth import get_current_user

metadata_router = APIRouter(prefix="/api/v1/metadata") 

@metadata_router.post("/update")
def update_metadata_route(metadata : Metadata , token : str = Depends(get_current_user)) : 
    return update_metadata(metadata)

@metadata_router.get("/")
def get_metadata_route(token : str = Depends(get_current_user)) : 
    return get_metadata()

@metadata_router.post("/emails") 
def save_new_email_route(email : str , token : str = Depends(get_current_user)) : 
    return add_new_email(email)

@metadata_router.delete("/emails")
def delete_email_route(email : str , token : str = Depends(get_current_user)) : 
    return delete_email(email)

@metadata_router.get("/emails") 
def get_emails(token : str = Depends(get_current_user)) :
    return load_emails()

@metadata_router.delete("/emails/{email}") 
def delete_email_route(email : str) :
    return delete_email(email)