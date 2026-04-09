from pydantic import BaseModel
from enum import Enum

class TokenSchema(BaseModel):
    access_token: str
    token_type: str

class Role(str, Enum):
    ADMIN = "admin"
    USER = "user"

class UserAuthSchema(BaseModel):
    tg_id: str
    role: Role