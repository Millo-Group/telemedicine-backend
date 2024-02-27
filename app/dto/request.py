from pydantic import BaseModel


class Req_DTO(BaseModel):
    data: str