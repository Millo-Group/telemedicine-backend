from fastapi import APIRouter, Request, Depends, HTTPException
from typing import Union
from ..dto.authanticate import Authenticate
from ..services.passport import decode_token, create_jwt_token

router = APIRouter()

@router.post('/authenticate')
async def authenticate(request: Request, item: Authenticate):
    odoo_service = request.state.odoo
    
    partner = odoo_service.get_partner_by_id(item.customer_id, ['contact_name'])
    employee = odoo_service.get_partner_by_id(item.employee_id, ['contact_name'])
    event = odoo_service.get_event_by_id(item.event_id, ['message_partner_ids'])

    partner_ids = event['message_partner_ids']

    if(partner is None or employee is None or item.customer_id not in partner_ids or item.employee_id not in partner_ids):
        raise HTTPException(
            status_code=401,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {'token': create_jwt_token({'employee': employee, 'partner': partner })}

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