# app/services/odoo_service.py

from xmlrpc.client import ServerProxy
from ..config import Settings

class OdooService:

    field_by_operation = {
        'subjective': 'digital_data_subjective_speech_text',
        'objective': 'digital_data_objective_speech_text',
        'assessment': 'digital_data_assessment_speech_text',
        'plan': 'digital_data_plan_speech_text'    
    }

    def __init__(self, url, username, password):
        self.settings = Settings()
        self.url = url
        self.db = self.settings.DB_NAME
        self.username = username
        self.password = password        
        self.common = ServerProxy(f'{url}/xmlrpc/2/common', allow_none=True)
        self.uid = None
        self.models = ServerProxy(f"{url}/xmlrpc/2/object", allow_none=True)

    def authenticate(self):
        try: 
            if not (self.uid):
                self.uid = self.common.authenticate(self.db, self.username, self.password, {})
            if not (self.uid):
                raise ValueError("Authentication failed")
            return bool(self.uid)
        except Exception as e:
            print(e)
            raise ValueError("Authentication failed")


    def get_partners(self, domain=None, fields=None, limit=None, offset = None):
        self.authenticate()
       
        options = {}
        if(limit):
            options['limit'] = limit
        if(offset):
            options['offset'] = offset
        records =  self.models.execute_kw(
            self.db,
            self.uid,
            self.password,
            'res.partner',
            'search_read',
            [domain or [], fields or []],
            options
        )

        return records
    
    def get_partner_by_id(self, id:int, fields = None):
        self.authenticate()
        record = self.models.execute_kw(
            self.db,
            self.uid,
            self.password, 
            'res.partner', 
            'read', 
            [id],
            {'fields': fields or []}
        )
        if len(record) == 0:
            return None
        return record[0]
    
    def get_employees(self, domain=None, fields=None, limit=None, offset = None):
        self.authenticate()
       
        options = {}
        if(limit):
            options['limit'] = limit
        if(offset):
            options['offset'] = offset
        records =  self.models.execute_kw(
            self.db,
            self.uid,
            self.password,
            'hr.employee.public',
            'search_read',
            [domain or [], fields or []],
            options
        )

        return records
    
    def get_employee_by_id(self, id:int, fields = None):
        self.authenticate()
        record = self.models.execute_kw(
            self.db,
            self.uid,
            self.password, 
            'hr.employee.public',
            'read', 
            [id], 
            {'fields': fields or []}
        )
        if len(record) == 0:
            return None
        return record[0]
    
    def get_events(self, domain=None, fields=None, limit=None, offset = None):
        self.authenticate()
       
        options = {}
        if(limit):
            options['limit'] = limit
        if(offset):
            options['offset'] = offset

        records =  self.models.execute_kw(
            self.db,
            self.uid,
            self.password,
            'calendar.event',
            'search_read',
            [domain or [], fields or []],
            options
        )

        return records
    
    def get_event_by_id(self, id:int, fields = None):
        self.authenticate()
        record = self.models.execute_kw(
            self.db,
            self.uid,
            self.password, 
            'calendar.event', 
            'read', 
            [id], 
            {'fields': fields or []}
        )
        if len(record) == 0:
            return
        return record[0]
    
    def get_event_details(self, domain=None, fields = None):
            self.authenticate()
            record = self.models.execute_kw(
                self.db,
                self.uid,
                self.password, 
                'visit.type.line',
                'search_read', 
                [domain or []], 
                {'fields': fields or [], 'limit': 1}
            )
            if len(record) == 0:
                return
            return record[0]

    def create_event_details(self, id: int, fields = None):
                self.authenticate()
                record = self.models.execute_kw(
                    self.db,
                    self.uid,
                    self.password, 
                    'visit.type.line',
                    'write', 
                    [[id], fields or {}],  
                )
                return record