from fastapi import APIRouter
from passlib.context import CryptContext
from pydantic import BaseModel

auth_router = APIRouter()

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str

# Passlib Context
