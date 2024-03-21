from pydantic import BaseModel

from enum import Enum
 

class Event_Details(BaseModel):
    type: str
    value: str