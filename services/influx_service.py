
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS
from utils.env_factory import get_config
from db.influx_db_connection import get_influx_connection 
from schemas.schemas import MetricsPrediction
import datetime

bucket , org = get_config("INFLUX_DB_BUCKET")  , get_config("INFLUX_DB_ORG") 
client = get_influx_connection() 
write_api = client.write_api(write_options=SYNCHRONOUS)
query_api = client.query_api()
bucket_api = client.buckets_api()






def check_bucket_and_create(bucket_name ) : 
    bucket = bucket_api.find_bucket_by_name(bucket_name)

    if bucket : 
        print("Bucket exist")
    else : 
        retention_rules = influxdb_client.BucketRetentionRules(type="expire", every_seconds=0)
        
        created_bucket = bucket_api.create_bucket(bucket_name=bucket_name , retention_rules=retention_rules , org=org)
        print(f"Bucket created {created_bucket}")
        return created_bucket 
    



def save_prediction(instance_id , prediction : MetricsPrediction ) : 
    check_bucket_and_create(bucket)
    p = influxdb_client.Point("predicted_measurement") \
        .tag("type" , "prediction") \
        .tag("instance_id", instance_id) \
        .field("cpu_usage", prediction.cpu_usage) \
        .field("memory_usage" , prediction.memory_usage) \
        .time(prediction.timestamp) 
    write_api.write(bucket=bucket, org=org, record=p)
    
    return p

def save_actual_records(instance_id , cpu_usage , memory_usage , timestamp) : 
    check_bucket_and_create(bucket)
    p = influxdb_client.Point("real_measurement") \
        .tag("type" , "actual") \
        .tag("instance_id", instance_id) \
        .field("cpu_usage", cpu_usage ) \
        .field("memory_usage" , memory_usage ) \
        .time(timestamp) 
    write_api.write(bucket=bucket, org=org, record=p)
    return p



def load_metrics(instance_id , start_time , measurment ) : 
    check_bucket_and_create(bucket)
    query = f'''
        from(bucket : "{bucket}")
        |> range(start : {start_time}) 
        |> filter(fn: (r) => r._measurement == "{measurment}") 
        |> filter(fn: (r) => r.instance_id == "{instance_id}") 
        '''
    
    result = query_api.query(org=org , query=query)
    results = []

    cpu_usage_table , memory_usage_table= result
    cpu_usage_table_records , memory_usage_table_records = cpu_usage_table.records , memory_usage_table.records


    for i in range(len(cpu_usage_table_records)) : 
        result_dict = { }

        result_dict['time'] = cpu_usage_table_records[i].get_time()
        result_dict[cpu_usage_table_records[i].get_field()] = cpu_usage_table_records[i].get_value()
        result_dict[memory_usage_table_records[i].get_field()] = memory_usage_table_records[i].get_value()
        
        results.append(result_dict)


    return results



