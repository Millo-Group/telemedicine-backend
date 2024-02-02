from pydantic import BaseModel

class Authenticate(BaseModel):
    employee_id: int
    customer_id: int
    event_id: int