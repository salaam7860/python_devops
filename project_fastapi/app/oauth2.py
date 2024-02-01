from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login") # PICK THE URL FROM THE ROUTES 

# SECRET KEY
# ALGORITHM
# EXPIRATION TIME

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# CREATE A TOKEN
def create_token(data: dict):
    to_encode = data.copy()

    # CREATE TIME EXPIRATION 
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    # CREATE JWT TOKEN #### DATA, ALGORITHM AND SECRET KEY 
    encoded_token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_token

# VERIFY THE ACCESS TOKEN 

def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id = str(payload.get("user_id")) # GET THE USER ID FROM auth.login.access_token

        if id is None:
            raise credentials_exception
        
        # VERIFY THE TOKEN DATA FROM THE SCHEMA 
        token_data = schemas.TokenData(id=id)
    except JWTError:
        raise credentials_exception
    
    return token_data

def get_current_user(token: str= Depends(oauth2_scheme)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"})

    return verify_access_token(token, credentials_exception)