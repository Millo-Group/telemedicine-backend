from fastapi import APIRouter, Request, Depends, HTTPException
from typing import Union

import string
import random

from ..dto.authanticate import Authenticate
from ..services.passport import decode_token, create_jwt_token
from ..services.jaas_jwt import JaaSJwtBuilder

 

router = APIRouter()
jwtBuilder = JaaSJwtBuilder()

@router.post('/authenticate')
async def authenticate(request: Request, item: Authenticate):
    odoo_service = request.state.odoo
    
    partner, employee = None, None

    if(item.customer_id):
        partner = odoo_service.get_partner_by_id(item.customer_id, ['name', 'email'])
    if(item.employee_id):
        employee = odoo_service.get_partner_by_id(item.employee_id, ['name', 'email'])
    
    event = odoo_service.get_event_by_id(item.event_id, ['message_partner_ids', 'name'])

    partner_ids = event['message_partner_ids']
    room_name = event['name'].replace(' ', '').lower() or ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))

    isNotUser = partner is None and employee is None
    id = item.customer_id or item.employee_id

    isEmployee = employee is not None

    if(isNotUser or id not in partner_ids):
        raise HTTPException(
            status_code=401,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user = employee or partner
    token = create_jwt_token({'user': user})

    jitsi_jwt = jwtBuilder.get_token(user['email'], user['name'], room_name, isEmployee)

    return {'token': token, 'jitsi_jwt': jitsi_jwt, 'room_name': room_name}
# get employees
@router.get('/employees')
async def get_employees(request: Request, skip:  Union[int, None] = None, limit: Union[int, None] = None, current_user: dict = Depends(decode_token)):
    odoo_service = request.state.odoo
    records = odoo_service.get_employees(None, None, limit, skip)
    return records

@router.get('/employees/{id}')
async def get_employee_by_id(request: Request, id: int, skip:  Union[int, None] = None, limit: Union[int, None] = None, current_user: dict = Depends(decode_token)):
    odoo_service = request.state.odoo
    record = odoo_service.get_employee_by_id(id)
    return record

@router.get('/partners')
async def get_partners(request: Request, skip:  Union[int, None] = None, limit: Union[int, None] = None, current_user: dict = Depends(decode_token)):
    print(current_user)
    odoo_service = request.state.odoo
    records = odoo_service.get_partners(None, None, limit, skip)
    return records

@router.get('/partners/{id}')
async def get_partner_by_id(request: Request, id: int, current_user: dict = Depends(decode_token)):
    odoo_service = request.state.odoo
    record = odoo_service.get_partner_by_id(id)
    return record

@router.get('/events')
async def get_events(request: Request, skip: int | None = None, limit: int | None = None, current_user: dict = Depends(decode_token)):
    odoo_service = request.state.odoo
    records = odoo_service.get_events(None, None, limit, skip)
    return records

@router.get('/events/{id}')
async def get_event_by_id(request: Request, id: int, current_user: dict = Depends(decode_token)):
    odoo_service = request.state.odoo
    records = odoo_service.get_event_by_id(id)
    return records
