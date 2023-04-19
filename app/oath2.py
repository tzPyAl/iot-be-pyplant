from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from . import schemas, database, models, config

oath2_scheme = OAuth2PasswordBearer(tokenUrl='login')

def create_access_token(data: dict):
    to_encode = data.copy()
    expires = datetime.utcnow() + timedelta(minutes=config.settings.ACCESS_TOKEN_EXPIRE_TIME)
    to_encode.update({"exp": expires})
    encoded_jwt = jwt.encode(to_encode, config.settings.SECRET_KEY, algorithm=config.settings.ALGORITHM)
    return encoded_jwt

def verify_access_token(token: str, credential_exception):
    try:
        payload = jwt.decode(token, config.settings.SECRET_KEY, algorithms=[config.settings.ALGORITHM])
        id: str = payload.get("user_id")
        if not id:
            raise credential_exception
        token_data = schemas.TokenData(id=id) # token_data is only id
    except JWTError as e:
        print(e)
        raise credential_exception
    except AssertionError as e:
        print(e)
    return token_data
    
def get_current_user(token: str = Depends(oath2_scheme), db: Session = Depends(database.get_db)):
    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                                         detail="Could not validate credentials", 
                                         headers={"WWW-Authenticate": "Bearer"})
    token = verify_access_token(token, credential_exception)
    user = db.query(models.Users).filter(models.Users.id == token.id).first()
    return user
