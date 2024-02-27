from pydantic import BaseModel, ConfigDict, HttpUrl

from enum import Enum
 
class Type(Enum):
    REFERRALS = 'REFERRALS'
    LABS = 'LABS'
    ERX = 'eRX'
    IMAGE = 'IMAGE'

class Report_DTO(BaseModel):
    model_config = ConfigDict(use_enum_values=True)
    patient_id: int
    type: Type
    file: HttpUrl