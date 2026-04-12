###############################################################################
####    Copy Right 2026 (C) Mohamed EL AFIA                             
####    App Name : Ouma                               
###############################################################################

from fastapi import FastAPI 
from routers.instances_router import instances_routers
from routers.incident_router import incident_router
from apscheduler.schedulers.background import BackgroundScheduler
from services.ressource_prediction_services import predict_next_and_save , is_prediction_service_ready 
from services.prometheus_service import fetch_metrics 

sched =  BackgroundScheduler()
app = FastAPI()


@sched.scheduled_job('interval' , id='my_job_id',  minutes=5)
def prediction_jon() : 
    if is_prediction_service_ready() :
        metrics = fetch_metrics()
        print("doing job...")
        
        predict_next_and_save(metrics)

    else : 
        print("Prediction services not ready to predict next values, cause the prediction requires past 24 values")

try :
    sched.start()
except : 
    sched.shutdown()
app.include_router(incident_router)
app.include_router(instances_routers)


