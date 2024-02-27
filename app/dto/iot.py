from pydantic import BaseModel, ConfigDict

from enum import Enum
 
class Type(Enum):
    TEMP = 'TEMPERATURE'
    BP = 'BP'
    PO2 = 'PO2'
    WEIGHT = 'WEIGHT'

class IOT_DTO(BaseModel):
    model_config = ConfigDict(use_enum_values=True)
    patient_id: int
    patient_name: str
    type: Type
    value: int