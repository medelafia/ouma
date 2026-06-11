###############################################################################
####    Copy Right 2026 (C) Mohamed EL AFIA                             
####    App Name : Ouma                               
###############################################################################

from fastapi import FastAPI , Depends ,HTTPException , Response
from routers.instances_router import instances_routers
from routers.incident_router import incident_router
from apscheduler.schedulers.background import BackgroundScheduler
from services.ressource_prediction_services import predict_next_and_save_by_xgboost , is_xgboost_prediction_engine_ready  , structurize 
from services.alerting_services import get_alerts_count , get_overview
from services.anomaly_service import get_anomalies_count
from services.incident_services import get_incidents_count 
from services.prometheus_service import fetch_instances
from services.prometheus_service import fetch_metrics 
from routers.alert_router import alerts_router
from routers.anomaly_router import anomaly_router
from fastapi.security import OAuth2PasswordRequestForm
from services.user_services import get_user_by_username , create_admin_user
from auth.auth import create_access_token , check_user_password , get_current_user
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from services.metadata_services import get_metadata
from routers.metadata_router import metadata_router
from utils.instance_factory import get_instance_by_host_and_port
from services.influx_service import save_actual_records 
import datetime
from db.mysql_db_connection import create_db_and_tables 
from services.email_services import create_emails_table
from services.system_services import check_system_health
import logging


@asynccontextmanager
async def lifespan(app : FastAPI) :
    await create_db_and_tables()
    create_admin_user()
    create_emails_table()
    logger.info("Startup")
    yield
    logger.info("shuting down")


sched =  BackgroundScheduler()
app = FastAPI(lifespan=lifespan)
interval = int(get_metadata().PREDICTION_INTERVAL)
logger = logging.getLogger(__name__)

@sched.scheduled_job('interval' , id='my_job_id',  minutes=1)
def prediction_job() : 
    metrics = fetch_metrics()
    logger.info("Doing job...")
    data = {}
    for metric in metrics : 
        if metric['name'] == "CPU usage " or metric['name'] == "Memory usage " : 
            for res in metric['value']['data']['result'] : 
                instance = get_instance_by_host_and_port(res['metric']['instance'].split(":")[0] ,res['metric']['instance'].split(":")[1] )
                instance_id = instance.instance_id
                timestamp = datetime.datetime.fromtimestamp(res['values'][-1][0], tz=datetime.timezone.utc)
                if instance_id in data : 
                    data[instance_id].update({metric['name'].lower().split()[0] : float(res['values'][-1][1]) , "timestamp" :  timestamp})
                else: 
                    data[instance_id] = {metric['name'].lower().split()[0] : float(res['values'][-1][1]) , "timestamp" :  timestamp}
                
    for instance_id in data : 
        logger.info(f"inserting value {str(save_actual_records(instance_id , data[instance_id]['cpu'] , data[instance_id]['memory'] , data[instance_id]['timestamp'] ))}")
    
    structured_data = structurize(metrics)

    if is_xgboost_prediction_engine_ready(structured_data) :
        predict_next_and_save_by_xgboost(structured_data)
    else : 
        logger.info("Xgboost Prediction engine not ready to predict next values, cause the prediction engine requires past 5 values")

    """ Multi modal feature disabled
    if is_cnn_lstm_prediction_engine_ready(structured_data) : 
        predict_next_and_save_by_cnn_lstm(cnn_lstm_data)
    else : 
        print("INFO: Cnn+BILstm Prediction engine not ready to predict next values, cause the prediction engine requires past 40 values")
    """
try :
    sched.start()
except : 
    sched.shutdown()


@app.post("/api/v1/auth/token")
async def login_for_access_token(response : Response , form_data: OAuth2PasswordRequestForm = Depends()):
    user = get_user_by_username(form_data.username)
    if user is None or not check_user_password( form_data.password , user.password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token = create_access_token(data={"sub": user.username})

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=False, # HTTPS only
        samesite="lax",
        max_age=1800
    )
    return {"status" : "success"}



@app.get("/api/v1/users/me")
def get_users_me(user : dict = Depends(get_current_user)) : 
    return { "username" :user['username'] , "message" : "This is a protected route"}

@app.get("/api/v1/kpis") 
def get_kpis(token : dict = Depends(get_current_user)) :
    return 
@app.get("/api/v1/overview") 
def get_overview_route(from_date : str ,user : dict = Depends(get_current_user) ) : 
    return  { 
                "statistics" : get_overview(datetime.datetime.fromisoformat(from_date[:-1]).replace(tzinfo=datetime.timezone.utc).date()) ,
                "kpis" : {
                    "anomalies" : get_anomalies_count() , 
                    "instances" : len(fetch_instances()) , 
                    "incidents" : get_incidents_count() , 
                    "alerts" : get_alerts_count()
                }
            }
@app.get("/api/v1/systemHealth")
def get_system_status() : 
    return check_system_health()
@app.get("/health")
def health():
    return {"status": "ok"}

app.add_middleware(
    middleware_class=CORSMiddleware , 
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=['*']
)
app.include_router(incident_router)
app.include_router(instances_routers)
app.include_router(anomaly_router)
app.include_router(alerts_router)
app.include_router(metadata_router)

