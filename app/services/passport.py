from fastapi import Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from ..config import Settings
from datetime import datetime, timedelta

ALGORITHM = 'HS256'

# OAuth2PasswordBearer is a dependency that can be used to get the token from the request header
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
settings = Settings()
# Function to decode the JWT token
def decode_token(request:Request, token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[ALGORITHM])

        employee = payload['employee']
        partner = payload['partner']
        
        if(payload['employee'] is None or payload['partner'] is None):
             raise credentials_exception
        
        odoo_service = request.state.odoo

        partner_data = odoo_service.get_partner_by_id(partner['id'], ['contact_name'])
        employee_data = odoo_service.get_employee_by_id(employee['id'], ['name'])

        if(partner_data is None or employee_data is None):
             raise credentials_exception
        
        return payload
    except JWTError:
        raise credentials_exception

def create_jwt_token(data: dict, expires_delta: timedelta = None):
    """
    Create a JWT token with the provided data and optional expiration time.
    """
    # to_encode = data.copy()

    # if expires_delta:
    #     expire = datetime.utcnow() + expires_delta
    # else:
    #     expire = datetime.utcnow() + timedelta(hours=2)  # Default expiration time

    # to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(data, settings.JWT_SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt
