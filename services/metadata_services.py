from db.sqlite_db_connection import get_connection 
import sqlite3 
from utils.env_factory import get_config



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

metadata = None
create_metadata_table()

def get_metadata(name) : 
    if metadata is None : 
        print("metadata not found, loading from db") 
        load_metadata()

    return metadata[name]

def get_metadata_from_db(name) : 
    with get_connection("db/metadata.db") as con :
        try: 
            cursor = con.cursor()   
            cursor.execute("SELECT * FROM Metadata WHERE name=?" , (name,))
            return cursor.fetchone()[1]
        except sqlite3.Error as err : 
            print(err) 
        
        finally : 
            cursor.close()

def set_metadata(name , new_value) : 
    with get_connection("db/metadata.db") as con :
        try: 
            cursor = con.cursor()   
            cursor.execute("UPDATE Metadata SET value=:new_value WHERE name=:name" , {new_value : new_value , name : name})
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
        metadata = {}
        for i in ['TARGET_SERVER_HOST' , 'PREDICTION_INTERVAL' ,'ACTIVATE_ALERTING' ] : 
            founded_value = get_metadata_from_db(i)

            if founded_value is None : 
                print("saving " +  get_config(i) + " to " + i)
                save_metadata(i , get_config(i))
                metadata[i] = get_config(i)
            else : 
                print(i + " founded " + founded_value)
                metadata[i] = founded_value
    return metadata