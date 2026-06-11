from fastapi import HTTPException
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS
from utils.env_factory import get_config
from db.influx_db_connection import get_influx_connection 
from schemas.schemas import MetricsPrediction
from datetime import datetime, timezone
import logging


bucket , org = get_config("INFLUX_DB_BUCKET")  , get_config("INFLUX_DB_ORG") 
client = get_influx_connection() 
write_api = client.write_api(write_options=SYNCHRONOUS)
query_api = client.query_api()
bucket_api = client.buckets_api()
delete_api = client.delete_api()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def check_bucket_and_create(bucket_name ) : 
    bucket = bucket_api.find_bucket_by_name(bucket_name)

    if bucket : 
        print("INFO:Bucket exist")
    else : 
        retention_rules = influxdb_client.BucketRetentionRules(type="expire", every_seconds=0)
        
        created_bucket = bucket_api.create_bucket(bucket_name=bucket_name , retention_rules=retention_rules , org=org)
        logger.info(f"Bucket created {str(created_bucket)}")
        return created_bucket 
    
def save_prediction( prediction : MetricsPrediction ) : 
    check_bucket_and_create(bucket)
    if prediction.instance_id is None : 
        raise ValueError("Cannot save a prediction with none instance id attribute") 
    p = influxdb_client.Point("predicted_measurement") \
        .tag("instance_id", str(prediction.instance_id)) \
        .field("cpu_usage_pred", prediction.cpu_usage) \
        .field("memory_usage_pred" , prediction.memory_usage) \
        .time(prediction.timestamp , write_precision="ns") 
    write_api.write(bucket=bucket, org=org, record=p)
    
    return p

def save_actual_records(instance_id , cpu_usage , memory_usage , timestamp) : 
    check_bucket_and_create(bucket)
    if instance_id is None : 
        raise ValueError("Cannot save a prediction with none instance id attribute") 
    p = influxdb_client.Point("real_measurement") \
        .tag("instance_id", str(instance_id)) \
        .field("cpu_usage_actual", cpu_usage ) \
        .field("memory_usage_actual" , memory_usage ) \
        .time(timestamp ,write_precision="ns") 
    write_api.write(bucket=bucket, org=org, record=p)
    return p

def load_metrics(instance_id , start_time , measurment ) : 
    check_bucket_and_create(bucket)
    query = f'''
        from(bucket : "{bucket}")
        |> range(start : {start_time.isoformat()}) 
        |> filter(fn: (r) => r._measurement == "{measurment}") 
        |> filter(fn: (r) => r.instance_id == "{instance_id}") 
        |> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")
        |> sort(columns: ["_time"])
        '''
    result = query_api.query(org=org, query=query)

    results = []

    metric_suffix = "actual" if measurment == "real_measurement" else "pred"
    for table in result:
        for record in table.records:
            result_dict = {
                "time": record.get_time(),
                "cpu_usage": record.values.get(f"cpu_usage_{metric_suffix}"),
                "memory_usage": record.values.get(f"memory_usage_{metric_suffix}")
            }
            results.append(result_dict)

    return results


def load_all_metrics(instance_id , start_time ) : 
    check_bucket_and_create(bucket)
    try : 
        query = f'''
            import "join"

            reals = from(bucket : "{bucket}")
            |> range(start : time(v: "{start_time.isoformat()}")) 
            |> filter(fn: (r) => r._measurement == "real_measurement" )
            |> filter(fn: (r) => r.instance_id == "{instance_id}") 
            |> keep(columns: ["_time", "_field", "_value", "instance_id"])
            |> pivot(rowKey:["_time","instance_id"], columnKey: ["_field"], valueColumn: "_value")
            

            predictions = from(bucket : "{bucket}")
            |> range(start : time(v: "{start_time.isoformat()}")) 
            |> filter(fn: (r) => r._measurement == "predicted_measurement") 
            |> filter(fn: (r) => r.instance_id == "{instance_id}") 
            |> keep(columns: ["_time", "_field", "_value", "instance_id"])
            |> pivot(rowKey:["_time","instance_id"], columnKey: ["_field"], valueColumn: "_value")

            join.inner(
                left: reals, 
                right: predictions, 
                on: (l, r) => l._time == r._time and l.instance_id == r.instance_id,
                as: (l, r) => ({{
                    time: l._time,
                    instance_id: l.instance_id,
                    cpu_usage_actual: l.cpu_usage_actual,
                    memory_usage_actual: l.memory_usage_actual,
                    cpu_usage_pred: r.cpu_usage_pred,
                    memory_usage_pred: r.memory_usage_pred
                }})
            )
            '''
        result = query_api.query(org=org, query=query)
        results = []

        for table in result:
            for record in table.records:
                result_dict = {
                    "time": record.values.get("time"),
                    "cpu_usage_actual": record.values.get("cpu_usage_actual"),
                    "memory_usage_actual": record.values.get("memory_usage_actual"),  
                    "cpu_usage_pred" : record.values.get("cpu_usage_pred"), 
                    "memory_usage_pred": record.values.get("memory_usage_pred"),  
                }
                results.append(result_dict)

        return results
    except Exception as ex :
        return []


def delete_all_metrics_by_instance_id(instance_id) :

    check_bucket_and_create(bucket)

    print(datetime.now().replace(tzinfo=timezone.utc).isoformat())
    delete_api.delete(
        start="1970-01-01T00:00:00Z",
        stop=f"{datetime.now().replace(tzinfo=timezone.utc).isoformat()}",
        predicate=f'_measurement="real_measurement" AND instance_id="{instance_id}"', 
        org=org,
        bucket=bucket
    )
    delete_api.delete(
        start="1970-01-01T00:00:00Z",
        stop=f"{datetime.now().replace(tzinfo=timezone.utc).isoformat()}",
        predicate=f'_measurement="predicted_measurement" AND instance_id="{instance_id}"', 
        org=org,
        bucket=bucket
    )

    return {
        "status" : "success"
    }
    