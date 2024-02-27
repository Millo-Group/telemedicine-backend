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
def decode_token(role:list = ['customer']):
    
    def decode_token_v2(request:Request, token: str = Depends(oauth2_scheme)):
        credentials_exception = HTTPException(
            status_code=401,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[ALGORITHM])
            
            if(payload['user'] is None):
                raise credentials_exception
            
            odoo_service = request.state.odoo

            id = payload['user']['id']
            
            partner_data = None
            employee_data = None

            if ('employee' in role):
                employee_data = employee_data = odoo_service.get_partner_by_id(id, ['contact_name'])
            if ('customer' in role):
                partner_data = odoo_service.get_partner_by_id(id, ['contact_name'])

            if(partner_data is None and employee_data is None):
                raise credentials_exception

            return payload
        except JWTError:
            raise credentials_exception
        except Exception as e:
            print(e)
    return decode_token_v2

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
