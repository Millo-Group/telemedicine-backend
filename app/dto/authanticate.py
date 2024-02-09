from pydantic import BaseModel, Field

class Authenticate(BaseModel):
    employee_id: int | None = Field(default=None, title="Employee id")
    customer_id: int | None = Field(default=None, title="Customer id")
    event_id: int