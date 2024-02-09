from fastapi import APIRouter, Request, Depends, HTTPException
from typing import Union
from ..dto.authanticate import Authenticate
from ..services.passport import decode_token, create_jwt_token

router = APIRouter()

