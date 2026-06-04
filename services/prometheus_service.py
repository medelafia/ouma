import requests 
import time 
from services.metadata_services import get_metadata , load_metadata
from schemas.schemas import Instance

## DEFINNING SOME GLOBAL VARIABLES 
loading_interval = load_metadata().PREDICTION_INTERVAL
PROMETHEUS_URL = f"http://{get_metadata().TARGET_SERVER_HOST}:{get_metadata().TARGET_SERVER_PORT}/api/v1"
queries = [
    { "name":"CPU cores" , "query" : 'count without(cpu, mode) (node_cpu_seconds_total{mode="idle"})' } , 
    {"name" :"CPU usage " , "query" : f'100 - (avg by (instance) (rate(node_cpu_seconds_total{{mode="idle"}}[{loading_interval}m])) * 100)'},
    { "name": "Memory capacity provisioned KB" , "query" : "node_memory_MemTotal_bytes / 1024"} , 
    { "name"  : "Memory usage " , "query": "(node_memory_MemTotal_bytes - node_memory_MemAvailable_bytes) / node_memory_MemTotal_bytes * 100"} , 
    { "name": "Disk read throughput KB/s" , "query": f"avg by (instance) (rate(node_disk_read_bytes_total[{loading_interval}m]))"} , 
    { "name": "Disk write throughput KB/s" , "query": f"avg by (instance) (rate(node_disk_written_bytes_total[{loading_interval}m]))"} , 
    { "name" : "Disk size GB" , "query" : 'sum by (instance) (node_filesystem_size_bytes{device=~"/dev/mapper/ocivolume-oled|/dev/mapper/ocivolume-root"} / 1024 / 1024 / 1024)'} ,
    #{ "name" : "Disk size GB" , "query" : 'avg by (instance,device) (node_filesystem_size_bytes{device="/dev/vda1"} / 1024 / 1024 / 1024)'} ,
    { "name" : "Network received throughput KB/s" , "query" : f'sum by (instance) (rate(node_network_receive_bytes_total[{loading_interval}m])) / 1024'}
]


def execute_query(path , query=None , is_range = False ) : 
    """
        Aim's for executing prometheus queries. 
        args : 
            - query : The query to execute
        return -> query result
    """
    try : 
        end = int(time.time())
        start = end - 1 * 45 * 60 

        if query is not None and is_range : 
            response = requests.get(path,params= { "query" : query, "step":loading_interval * 60, "start" : start ,"end" : end }) 
        elif query is not None : 
            response = requests.get(path, params={"query":query})
        else : 
            response = requests.get(path)
       
        response.raise_for_status()

        return response.json()
    except Exception as ex: 
        print(ex)

def fetch_metrics() : 
    """
        Metrics loader from prometheus instance, return a list of metrics
    """
    responses_metrics= [  {"name" : query['name'] , "value" :  execute_query(PROMETHEUS_URL + "/query_range" , query['query'] , is_range=True)} for query in queries ] 
    return responses_metrics 

def fetch_instance_metrics(instance_host) : 
    responses_metrics = fetch_metrics() 
    for metric in responses_metrics : 
        if metric['value']['status'] :
            for i , result in enumerate(metric['value']['data']['result']) : 
                if result['metric']['instance'] != instance_host : 
                    metric['value']['data']['result'].pop(i)
    
    return responses_metrics

def fetch_instances() : 
    json_response = execute_query(PROMETHEUS_URL + "/targets")
    services = [service for service in json_response['data']['activeTargets'] if service['labels']['job'] == "node-exporter"] 
    return services

def fetch_instance_ressources(instance : Instance ) :
    instance = instance.ip_address + ":" + str(instance.port)
    cpu_result = execute_query(PROMETHEUS_URL + "/query" ,f'100 - (avg by (instance) (rate(node_cpu_seconds_total{{mode="idle" , instance="{instance}"}}[5m])) * 100)' )
    mem_result = execute_query(PROMETHEUS_URL + "/query" ,f'(node_memory_MemTotal_bytes{{instance = "{instance}"}} - node_memory_MemAvailable_bytes{{instance = "{instance}"}}) / node_memory_MemTotal_bytes{{instance = "{instance}"}} * 100')


    cpu_val = float(cpu_result['data']['result'][0]['value'][1]) if cpu_result['status'] == 'success' else float('nan')
    memory_value = float(mem_result['data']['result'][0]['value'][1]) if cpu_result['status'] == 'success' else float('nan')

    return  cpu_val , memory_value 