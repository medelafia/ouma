from db.sqlite_db_connection import get_connection
import sqlite3
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from utils.env_factory import get_config
import ssl
from fastapi import HTTPException

context = ssl.create_default_context()

def create_emails_table() : 
    with get_connection("db/emails.db") as con :
        try : 
            cursor = con.cursor()   
            cursor.execute("CREATE TABLE IF NOT EXISTS Emails (" \
                "email TEXT PRIMARY KEY )" \
            )
            con.commit()
            cursor.close()
        except sqlite3.Error as err : 
            print(err)

def add_new_email(email) :
    with get_connection("db/emails.db") as con : 
        try : 
            cursor = con.cursor()   
            cursor.execute("INSERT INTO Emails VALUES (?)" , (email ,)) 
            con.commit()
        except sqlite3.Error as err : 
            exception = HTTPException(
                status_code=500,
                detail= "Email already exist"
            )
            raise exception
        finally : 
            cursor.close()

def load_emails() : 
    with get_connection("db/emails.db") as con : 
        try : 
            cursor = con.cursor()   
            cursor.execute("SELECT * FROM Emails")  
            return [ row[0] for row in cursor.fetchall() ]
        except sqlite3.Error as err : 
            print(err)
        finally : 
            cursor.close() 
        
def delete_email(email) :
    with get_connection("db/emails.db") as con : 
        try : 
            cursor = con.cursor()   
            cursor.execute("DELETE FROM Emails WHERE email=?" , (email ,)) 
            con.commit()
            return {"status" : "success"}
        except sqlite3.Error as err : 
            print(err)
        finally : 
            cursor.close()


def notify_admins_by_emails(subject , body ) : 

    system_email = get_config("SYSTEM_EMAIL")
    smtp_server = get_config("SMTP_SERVER") 
    smtp_port = int(get_config("SMTP_PORT"))
    system_email_password = get_config("SYSTEM_EMAIL_PASSWORD")
    try :
        receipients = load_emails()
        msg = MIMEMultipart()
        msg['Subject'] = subject
        msg['From'] = system_email
        msg['To'] = ', '.join(receipients)
        msg.attach(MIMEText(body, 'plain'))
        with smtplib.SMTP(smtp_server, smtp_port) as smtp:
            smtp.starttls(context=context)
            smtp.login(system_email , system_email_password)
            smtp.sendmail(system_email, receipients , msg.as_string())

    except Exception as ex: 
        print(ex)