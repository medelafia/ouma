from db.influx_db_connection import get_influx_connection 
from models.models import Prediction
from influxdb_client.client.write_api import SYNCHRONOUS
from utils.env_factory import get_config




bucket , org = get_config("INFLUX_DB_BUCKET")  , get_config("INFLUX_DB_ORG") 
client = get_influx_connection() 
write_api = client.write_api(write_options=SYNCHRONOUS)

def save_prediction(node_id , prediction : Prediction ) : 
    p = influxdb_client.Point("predictions") \
        .tag("type" , "prediction") \
        .tag("node_id", node_id) \
        .field("cpu_usage", prediction.cpu_usage) \
        .field("memory_usage" , prediction.memory_usage) \
        .time(prediction.timestamp) 
    write_api.write(bucket=bucket, org=org, record=p)
    
    return p

def save_actual_records(node_id , cpu_usage , memory_usage , timestamp) : 
    p = influxdb_client.Point("predictions") \
        .tag("type" , "actual") \
        .tag("node_id", node_id) \
        .field("cpu_usage", cpu_usage ) \
        .field("memory_usage" , memory_usage ) \
        .time(timestamp) 
    write_api.write(bucket=bucket, org=org, record=p)
    
    return p



def load_actual_values(node_id) : 
    pass 



def load_predictions(node_id) : 
    pass 
