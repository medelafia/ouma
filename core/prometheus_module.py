import requests 
import json 
import time 


"""
    Copy Right 2026 (C) Mohamed EL AFIA                             
    Tool Name : Ouma  
    Purpose : Cycle End Project                               
"""



## DEFINNING SOME GLOBAL VARIABLES 
PROMETHEUS_URL = "http://localhost:9090/api/v1"
queries = [
    {"name" :"cpu_usage" , "query" : '100 - (avg by (instance) (rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)'},
    { "name"  : "memory_usage" , "query": "(node_memory_MemTotal_bytes - node_memory_MemAvailable_bytes) / node_memory_MemTotal_bytes * 100"} , 
   # { "name": "avalaible_memory" , "query": ""} , 
    { "name": "disk_read" , "query": "avg by (instance) (rate(node_disk_read_bytes_total[5m]))"} , 
    { "name": "disk_write" , "query": "avg by (instance) (rate(node_disk_written_bytes_total[5m]))"} , 
    { "name":"cpu_cores" , "query" : 'count without(cpu, mode) (node_cpu_seconds_total{mode="idle"})' } , 
]

def execute_query(path , query=None ) : 
    """
        Aim's for executing prometheus queries. 
        args : 
            - query : The query to execute
        return -> query result
    """
    try : 
        end = int(time.time())
        start = end - 2 * 60 * 60 

        response = requests.get(path,params= { "query" : query, "step":300, "start" : start ,"end" : end }) if query is not None else requests.get(path)
        response.raise_for_status()

        return response.json()
    except Exception as ex: 
        print(ex)

def fetch_metrics() : 
    """
        Metrics loader from prometheus instance, return a list of metrics
        args : 
            - nodes_id :
    """
    global metrics

    responses_metrics= [  {"name" : query['name'] , "value" :  execute_query(PROMETHEUS_URL + "/query_range" , query['query'])} for query in queries ] 
    

    return responses_metrics 


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



