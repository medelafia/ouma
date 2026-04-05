###############################################################################
####    Copy Right 2026 (C) Mohamed EL AFIA                             
####    App Name : Ouma                               
###############################################################################

from fastapi import FastAPI 
from routers.instances_router import instances_routers
from routers.incident_router import incident_router


app = FastAPI()
app.include_router(incident_router)
app.include_router(instances_routers)

