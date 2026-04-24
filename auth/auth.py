from fastapi.security import OAuth2PasswordBearer
from services.user_services import get_user_by_username, check_user_password
from utils.env_factory import get_config
from datetime import datetime ,timedelta
from jose import jwt , JWTError
from fastapi import Depends, HTTPException

SECRET_KEY = get_config("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/token") 


def create_access_token(data: dict ) : 
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode.update({"exp":expire})
    encoded_jwt = jwt.encode(to_encode , key=SECRET_KEY ,algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user(token : str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        return {"username" : username}
    except JWTError:
        raise credentials_exception