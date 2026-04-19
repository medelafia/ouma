from dotenv import load_dotenv 
import os
load_dotenv() 


variables = {
    "INFLUX_DB_BUCKET" : None, 
    "INFLUX_DB_ORG" : None , 
    "INFLUX_DB_TOKEN" : None , 
    "INFLUX_DB_URL" : None , 
    "MYSQL_USER" : None , 
    "MYSQL_PASSWORD" : None , 
    "MYSQL_DB" : None , 
    "MYSQL_HOST" : None,
    "SECRET_KEY": None
}

def get_config(variable_key) : 
    global variables 

    if any([val is None for key , val in variables.items()]) : 
        print("exec")
        for key in variables : 
            variables[key]= os.environ.get(key)
    
    return variables[variable_key]


