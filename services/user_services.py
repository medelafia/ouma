from models.models import User 
from sqlmodel import Session ,select 
from db.mysql_db_connection import get_engine
import bcrypt


def save_user(user : User ) : 
    with Session(get_engine()) as session : 
        user.password = bcrypt.hashpw(user.password.encode("utf-8") , bcrypt.gensalt())
        session.add(user) 
        session.commit()
    
        return user

def get_user_by_username(username):
    with Session(get_engine()) as session : 
        return session.exec(select(User).where(User.username == username)).first()
        
def check_user_password(user_password , password) : 
    with Session(get_engine()) as session : 
        return bcrypt.checkpw(password.encode("utf-8") , user_password.encode("utf-8"))


save_user(User(username="admin" , password="admin"))

