from db.sqlite_db_connection import get_connection 
import sqlite3 
from utils.env_factory import get_config
from schemas.schemas import Metadata
import logging 


logger = logging.getLogger(__name__ ) 


def create_metadata_table() : 
    with get_connection("db/metadata.db") as con :
        try : 
            cursor = con.cursor()   
            cursor.execute("CREATE TABLE IF NOT EXISTS Metadata (" \
            "name TEXT PRIMARY KEY," \
            "value TEXT );"
            )
            con.commit()
            cursor.close()
        except sqlite3.Error as err : 
            print(err)
        
def parse_value(value : str):
    if value.isnumeric() :
        return int(value) 
    elif value in ['True' , 'False'] :
        return bool(value) 
    else :
        return value


metadata = None
create_metadata_table()

def get_metadata() : 
    if metadata is None : 
        logger.info("metadata not found, loading from sqlite database") 
        load_metadata()

    return metadata

def get_metadata_from_db(name) : 
    with get_connection("db/metadata.db") as con :
        try: 
            cursor = con.cursor()   
            cursor.execute("SELECT * FROM Metadata WHERE name=?" , (name,))
            return cursor.fetchone()
        except sqlite3.Error as err : 
            print(err) 
        
        finally : 
            cursor.close()

def set_metadata(name , new_value) : 
    with get_connection("db/metadata.db") as con :
        try: 
            cursor = con.cursor()   
            cursor.execute("UPDATE Metadata SET value=? WHERE name=?" , (new_value , name))
            con.commit()
        except sqlite3.Error as err : 
            print(err) 
        
        finally : 
            cursor.close()

def save_metadata(name , value) : 
     with get_connection("db/metadata.db") as con :
        try: 
            cursor = con.cursor()    
            cursor.execute("INSERT INTO Metadata VALUES (?, ?)" , (name , value))
            con.commit()
        except sqlite3.Error as err : 
            print(err) 
        
        finally : 
            cursor.close()
        
def load_metadata() : 
    global metadata
    if metadata is None :
        metadata = Metadata()
        for i in ['TARGET_SERVER_HOST' , 'PREDICTION_INTERVAL' ,'ACTIVATE_EMAIL_ALERTING', 'ACTIVATE_SLACK_ALERTING', 'TARGET_SERVER_PORT' ] : 
            save_metadata(i , get_config(i))
            setattr(metadata, i , parse_value(get_config(i)))
    return metadata


def update_metadata( request_metadata : Metadata ) : 
    global metadata
    for i in ['TARGET_SERVER_HOST' , 'PREDICTION_INTERVAL' ,'ACTIVATE_EMAIL_ALERTING', 'ACTIVATE_SLACK_ALERTING', 'TARGET_SERVER_PORT' ] : 
        print(request_metadata.model_dump()[i]) 
        set_metadata(i , request_metadata.model_dump()[i])
        setattr(metadata , i, request_metadata.model_dump()[i])
    return metadata
