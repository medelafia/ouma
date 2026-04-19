###############################################################################
####    Copy Right 2026 (C) Mohamed EL AFIA                             
####    App Name : Ouma                               
###############################################################################

from fastapi import FastAPI , Depends ,HTTPException
from routers.instances_router import instances_routers
from routers.incident_router import incident_router
from apscheduler.schedulers.background import BackgroundScheduler
from services.ressource_prediction_services import predict_next_and_save , is_prediction_service_ready 
from services.prometheus_service import fetch_metrics 
from routers.alert_router import alerts_router
from routers.anomaly_router import anomaly_router
from fastapi.security import OAuth2PasswordRequestForm
from services.user_services import get_user_by_username
from auth.auth import create_access_token , check_user_password

sched =  BackgroundScheduler()
app = FastAPI()

@sched.scheduled_job('interval' , id='my_job_id',  minutes=1)
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


@app.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = get_user_by_username(form_data.username)
    if user is None or check_user_password(user.password , form_data.password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

app.include_router(incident_router)
app.include_router(instances_routers)
app.include_router(anomaly_router)
app.include_router(alerts_router)

