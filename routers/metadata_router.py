from fastapi import APIRouter 
from services.metadata_services import update_metadata , get_metadata 
from services.email_services import add_new_email , delete_email , load_emails
from schemas.schemas import Metadata

metadata_router = APIRouter(prefix="/api/v1/metadata") 

@metadata_router.post("/update")
def update_metadata_route(metadata : Metadata) : 
    return update_metadata(metadata)

@metadata_router.get("/")
def get_metadata_route() : 
    return get_metadata()

@metadata_router.post("/emails") 
def save_new_email_route(email : str) : 
    return add_new_email(email)

@metadata_router.delete("/emails")
def delete_email_route(email : str) : 
    return delete_email(email)

@metadata_router.get("/emails") 
def get_emails() :
    return load_emails()