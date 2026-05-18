from models.models import User 
from sqlmodel import Session ,select 
from db.mysql_db_connection import get_engine
import bcrypt


def save_user(user : User ) : 
    with Session(get_engine()) as session : 
        user.password = bcrypt.hashpw(user.password.encode("utf-8") , bcrypt.gensalt())
        session.add(user) 
        session.commit()
        print("user inserted" , user.username)
        return user

def get_user_by_username(username):
    with Session(get_engine()) as session : 
        return session.exec(select(User).where(User.username == username)).first()
        
def check_user_password(user_password , password) : 
    with Session(get_engine()) as session : 
        return bcrypt.checkpw(password.encode("utf-8") , user_password.encode("utf-8"))

def create_admin_user():
    with Session(get_engine()) as session:
        # Check if admin already exists
        result = session.exec(select(User).where(User.username == "admin"))
        if result.one_or_none():
            print("Admin user already exists")
            return

        # Create admin
        admin = User(
            username="admin",
            password=bcrypt.hashpw("admin".encode("utf-8") , bcrypt.gensalt()) 
        )
        session.add(admin)
        session.commit()
        print("Admin user created")


