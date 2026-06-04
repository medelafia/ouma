



def check_prometheus_health() :
    return True 

def check_influx_health() :
    return True 

def check_mysql_health() :
    return True 

def check_system_health() : 
    response = {}
    if not check_mysql_health() :
        response["mysql"] = "mysql unhealthy or down" 
    
    if not check_influx_health() : 
        response["influx"] = "influx unhealthy or down" 
    
    if not check_prometheus_health() : 
        response["prometheus"] = "prometheus unhealthy or down" 
    
    return response