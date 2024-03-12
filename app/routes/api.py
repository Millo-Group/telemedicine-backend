from fastapi import APIRouter, Request, Depends, HTTPException
from typing import Union
from datetime import datetime, timedelta
from pydantic import ValidationError

import string
import random
import json

from ..dto.authanticate import Authenticate
from ..dto.iot import IOT_DTO
from ..dto.report import Report_DTO
from ..dto.request import Req_DTO

from ..services.passport import decode_token, create_jwt_token
from ..services.jaas_jwt import JaaSJwtBuilder
from ..services.iot_service import IOTService
from ..services.report_service import ReportService
from ..services.crypto_service import CryptoService

router = APIRouter()
jwtBuilder = JaaSJwtBuilder()
iotService = IOTService()
reportService = ReportService()
cryptoService = CryptoService()

@router.post('/authenticate')
async def authenticate(request: Request, item: Req_DTO):
    try:
        odoo_service = request.state.odoo
        data = item.dict()['data']
        result = cryptoService.decryptDict(data)
        item = Authenticate(**result)

        partner = None
        employee = None

        if(item.customer_id):
            partner = odoo_service.get_partner_by_id(item.customer_id, ['name', 'email'])
        if(item.employee_id):
            employee = odoo_service.get_partner_by_id(item.employee_id, ['name', 'email', 'employee_ids'])
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
    except ValidationError as e:
        raise HTTPException(status_code=400,  detail=json.loads(e.json()))
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500)
# get employees
@router.get('/employees')
async def get_employees(request: Request, skip:  Union[int, None] = None, limit: Union[int, None] = None, current_user: dict = Depends(decode_token(['employee']))):
    odoo_service = request.state.odoo
    records = odoo_service.get_employees(None, None, limit, skip)
    return records

@router.get('/employees/{id}')
async def get_employee_by_id(request: Request, id: int, skip:  Union[int, None] = None, limit: Union[int, None] = None, current_user: dict = Depends(decode_token(['employee']))):
    odoo_service = request.state.odoo
    record = odoo_service.get_employee_by_id(id)
    return record

@router.get('/partners')
async def get_partners(request: Request, skip:  Union[int, None] = None, limit: Union[int, None] = None, current_user: dict = Depends(decode_token(['employee']))):
    odoo_service = request.state.odoo
    records = odoo_service.get_partners(None, None, limit, skip)
    return records

@router.get('/partners/{id}')
async def get_partner_by_id(request: Request, id: int, current_user: dict = Depends(decode_token(['employee', 'customer']))):
    odoo_service = request.state.odoo
    record = odoo_service.get_partner_by_id(id)
    return record

@router.get('/events')
async def get_events(request: Request, skip: int | None = None, limit: int | None = None, current_user: dict = Depends(decode_token(['employee', 'customer']))):
    odoo_service = request.state.odoo
    records = odoo_service.get_events(None, None, limit, skip)
    return records

@router.get('/events/{id}')
async def get_event_by_id(request: Request, id: int, current_user: dict = Depends(decode_token(['employee', 'customer']))):
    odoo_service = request.state.odoo
    records = odoo_service.get_event_by_id(id)
    return records

@router.get('/iot')
async def get_iot_data(request: Request, patient_id:int, current_user: dict = Depends(decode_token(['employee']))):
    db = request.state.db
    records = iotService.readByPatientId(db, patient_id)
    return records
    
@router.post('/iot')
async def create_iot_data(request: Request, item: Req_DTO, current_user: dict = Depends(decode_token(['employee']))):
        try:
            db = request.state.db
            data = item.dict()['data']
            result = cryptoService.decryptDict(data)
            IOT_DTO(**result)
            records = iotService.create(db, result)
            return records
        except ValidationError as e:
             raise HTTPException(status_code=400,  detail=json.loads(e.json()))
        except Exception as e:
            raise HTTPException(status_code=500)

@router.get('/reports')
async def get_report_data(request: Request, patient_id:int, current_user: dict = Depends(decode_token(['employee'])),):
    db = request.state.db
    records = reportService.readByPatientId(db, patient_id)
    return records
    
@router.post('/reports')
async def create_report_data(request: Request, item: Req_DTO, current_user: dict = Depends(decode_token(['employee']))):
        try:
            db = request.state.db
            data = item.dict()['data']
            result = cryptoService.decryptDict(data)
            Report_DTO(**result)
            records = reportService.create(db, result)
            return records
        except ValidationError as e:
             raise HTTPException(status_code=400,  detail=json.loads(e.json()))
        except Exception as e:
            print(e)
            raise HTTPException(status_code=500)

@router.get('/doctor/appointments')
async def get_appointments_data(request: Request, current_user: dict = Depends(decode_token(['employee']))):
    odoo_service = request.state.odoo
    doctor = current_user['user']

    today = datetime.now()
    start_of_week = today - timedelta(days=today.weekday())
    end_of_week = start_of_week + timedelta(days=6)

    search_domain = [
        ('start', '>=', start_of_week.strftime('%Y-%m-%d 00:00:00')),
        ('start', '<=', end_of_week.strftime('%Y-%m-%d 23:59:59')), 
        ('videocall_location', '!=', True), 
        ('doctore_id', 'in', doctor['employee_ids'])
    ]

    events = odoo_service.get_events(search_domain, None)
    return events
    