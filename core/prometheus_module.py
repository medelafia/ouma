import requests 
import json 



"""
    Copy Right 2026 (C) Mohamed EL AFIA                             
    app name : Smart Mon                                            
"""



## DEFINNING SOME GLOBAL VARIABLES 
PROMETHEUS_URL = "http://localhost:9090/api/v1"
metrics = [
    {"name" :"cpu_usage" , "query" : '100 - (avg by (instance) (irate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)'},
    { "name"  : "memory_usage" , "query": "(node_memory_MemTotal_bytes - node_memory_MemAvailable_bytes) / node_memory_MemTotal_bytes * 100"} , 
    { "name": "avalaible_memory" , "query": ""} , 
    { "name": "disk_read" , "query": "rate(node_disk_read_bytes_total[5m])"} , 
    { "name": "disk_write" , "query": "rate(node_disk_written_bytes_total[5m])"} , 
    { "name": "disk_storage" , "query": ""} , 
    { "name":"cpu_cores" , "query" : 'count without(cpu, mode) (node_cpu_seconds_total{mode="idle"})' } , 
]

def execute_query(path , query ) : 
    """
        Aim's for executing prometheus queries. 
        args : 
            - query : The query to execute
        return -> query result
    """
    try : 
    
        response = requests.get(path,params= { "query" : query}) if query is not None else requests.get(path)
        response.raise_for_status()

        return response.json()
    except Exception as ex: 
        print(ex)

def fetch_metrics(node_id) : 
    """
        Metrics loader from prometheus instance, return a list of metrics
        args : 
            - nodes_id :
    """

    metrics = [  {"name" : metric['name'] , "value" :  execute_query(PROMETHEUS_URL + "/query" , metric['name'])} for metric in metrics] 
    
    return metrics 


def fetch_nodes() : 
    """ 
        This function responsible for fetching services from eureka discovery
    """
    json_response = execute_query(PROMETHEUS_URL + "/targets")
    services = [service for service in json_response['data']['activeTargets']] 
    return services

def check_service_health(service_name) : 
    """
        This function responsible for checking service health , to assume monitoring
    """
    response = requests.get(PROMETHEUS_URL)
    return response



