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
    "SECRET_KEY": None , 
    "TARGET_SERVER_HOST" : None , 
    "PREDICTION_INTERVAL" : None , 
    "ACTIVATE_EMAIL_ALERTING" : None  , 
    "ACTIVATE_SLACK_ALERTING": None , 
    "TARGET_SERVER_PORT" : None , 
    "SYSTEM_EMAIL" : None ,  
    "SMTP_SERVER" : None , 
    "SMTP_PORT" : None , 
    "SYSTEM_EMAIL_PASSWORD" : None  , 
    "SLACK_TOKEN" : None , 
    "SLACK_CHANNEL" : None ,
    "SLACK_USER" : None 
} 

def get_config(variable_key) : 
    global variables 

    if any([val is None for key , val in variables.items()]) : 
        for key in variables : 
            variables[key]= os.environ.get(key)
    
    return variables[variable_key]


