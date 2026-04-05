from db.influx_db_connection import get_influx_connection 
from schemas.schemas import MetricsPrediction
from influxdb_client.client.write_api import SYNCHRONOUS
from utils.env_factory import get_config




bucket , org = get_config("INFLUX_DB_BUCKET")  , get_config("INFLUX_DB_ORG") 
client = get_influx_connection() 
write_api = client.write_api(write_options=SYNCHRONOUS)
query_api = client.query_api()

def save_prediction(instance_id , prediction : MetricsPrediction ) : 
    p = influxdb_client.Point("predicted_measurment") \
        .tag("type" , "prediction") \
        .tag("instance_id", instance_id) \
        .field("cpu_usage", prediction.cpu_usage) \
        .field("memory_usage" , prediction.memory_usage) \
        .time(prediction.timestamp) 
    write_api.write(bucket=bucket, org=org, record=p)
    
    return p

def save_actual_records(instance_id , cpu_usage , memory_usage , timestamp) : 
    p = influxdb_client.Point("real_measurement") \
        .tag("type" , "actual") \
        .tag("instance_id", instance_id) \
        .field("cpu_usage", cpu_usage ) \
        .field("memory_usage" , memory_usage ) \
        .time(timestamp) 
    write_api.write(bucket=bucket, org=org, record=p)
    
    return p



def load_metrics(instance_id , start_time , end_time , measurment ) : 
    query = f'from(bucket : {bucket})\
            range(start : ) \
            filtet(fn: (r) => r._measurment == {measurment}) \
            filter(fn: (r) => r.instance == {instance_id}) '
    
    result = query_api.query(org=org , query=query)
    results = []
    for table in result : 
        for record in table.records : 
            results.append((record.get_field() , record.get_value()))

    print(results) 
    return result 

