import sqlite3 




def get_connection(db_name) :
    return sqlite3.connect(f"./{db_name}")


