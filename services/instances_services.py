from db.sqlite_db_connection import get_connection
from schemas.schemas import Instance
import sqlite3

def create_database_and_table() : 
    with get_connection("db/instances.db") as con :
        try :
            cursor = con.cursor() 
            cursor.execute("CREATE TABLE IF NOT EXISTS instances (" \
                        "id TEXT PRIMARY KEY ," \
                        "host TEXT ,"\
                            "port INTEGER"
                        ");")
            con.commit()
            cursor.close()
        except sqlite3.Error as err : 
            print(err)


def load_instance_by_host_and_port(host , port) : 
    with get_connection("db/instances.db") as con : 
        try :
            cursor = con.cursor() 
            query = "SELECT * FROM instances WHERE host=:host and port=:port" ; 
            cursor.execute(query , {"host" : host , "port" : port})
            return cursor.fetchone()
    
        except sqlite3.Error as err : 
            print(err)

def save_instance(instance : Instance) :
    with get_connection("db/instances.db") as con : 
        
        cursor = con.cursor() 
        query = "INSERT INTO instances VALUES (:id , :host , :port) " ; 
        cursor.execute(query , {"id" : instance.instance_id , "host" : instance.ip_address , "port" : instance.port})
        con.commit()
    

