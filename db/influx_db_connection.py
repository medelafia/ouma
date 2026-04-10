import influxdb_client
from utils.env_factory import get_config


bucket = get_config("INFLUX_DB_BUCKET")
org = get_config("INFLUX_DB_ORG")
token = get_config("INFLUX_DB_TOKEN")
# Store the URL of your InfluxDB instance
url=get_config("INFLUX_DB_URL")


def get_influx_connection(): 
    client = influxdb_client.InfluxDBClient(
        url=url,
        token=token,
        org=org
        )
    return client  

