import mysql.connector 
from utils.env_factory import get_config

 

HOST , _ = get_config("MYSQL_DB_HOST").split(":")
USERNAME = get_config("MYSQL_DB_USERNAME")
PASSWORD = get_config("MYSQL_DB_PASSWORD")


def get_mysql_connection() : 
    return mysql.connector.connect(
        host=HOST,
        user=USERNAME,
        password=PASSWORD
        )
