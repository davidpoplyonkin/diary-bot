from fastapi import FastAPI, Depends, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from starlette import status
from typing import Annotated
import hashlib
import hmac
import jwt
from urllib.parse import parse_qsl
import json
from datetime import datetime, timezone, timedelta
from time import time
import os

TG_TOKEN = os.getenv("TG_TOKEN", "")
ADMIN_TG_ID = os.getenv("ADMIN_TG_ID", "")
API_ALLOW_ORIGINS = os.getenv("API_ALLOW_ORIGINS", "").split(",")
JWT_SECRET = os.getenv("JWT_SECRET", "")
JWT_ALGORITHM = "HS256"
JWT_EXP_SECONDS = 1800


app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=API_ALLOW_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Token(BaseModel):
    access_token: str
    token_type: str

@app.post("/auth/token", response_model=Token)
async def issue_token(x_telegram_init_data: Annotated[str, Header()]):
    """
    Exchange Telegram InitData for a JWT
    """
    init_data_invalid = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid Telegram Init Data",
    )
    init_data_expired = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Expired Telegram Init Data",
    )

    # Parse Telegram InitData
    # https://core.telegram.org/bots/webapps#validating-data-received-via-the-mini-app
    init_data_dict = dict(parse_qsl(x_telegram_init_data))

    try:
        init_data_hash = init_data_dict.pop("hash")
    except KeyError:
        raise init_data_invalid
    
    # Derive the string encrypted by Telegram
    data_check_string = "\n".join(
        f"{k}={v}" for k, v in sorted(init_data_dict.items())
    )

    # Derive the key used by Telegram
    secret_key = hmac.new(
        b"WebAppData", 
        TG_TOKEN.encode(), 
        hashlib.sha256
    ).digest()

    # Calculate the authentic hash
    calculated_hash = hmac.new(
        secret_key, 
        data_check_string.encode(), 
        hashlib.sha256
    ).hexdigest()

    # Ensure that the hashes match
    if not hmac.compare_digest(calculated_hash, init_data_hash):
        raise init_data_invalid
    
    # Check if InitData is expired using the same threshold as for JWT
    if int(time()) - int(init_data_dict.get("auth_date", 0)) > JWT_EXP_SECONDS:
        raise init_data_expired
    
    user = json.loads(init_data_dict.get("user"))
    
    payload = {
        "sub": str(user.get("id")),
        "exp": datetime.now(timezone.utc) + timedelta(seconds=JWT_EXP_SECONDS),
    }

    # Generate the token
    token = jwt.encode(
        payload,
        JWT_SECRET,
        algorithm=JWT_ALGORITHM
    )
    
    return {
        "access_token": token,
        "token_type": "bearer"
    }

http_bearer = HTTPBearer()

class User(BaseModel):
    id: str

async def validate_token(auth: Annotated[HTTPAuthorizationCredentials, Depends(http_bearer)]) -> User:
    """
    Check the JWT and return the current user
    """

    token = auth.credentials

    # Validate Token
    try:
        payload = jwt.decode(
            token, 
            JWT_SECRET, 
            algorithms=[JWT_ALGORITHM],
            options={"require": ["exp", "sub"]}
        )
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Expired Token",
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token",
        )
    
    return {"id": payload.get("sub")} # fetch the user

async def admin_only(user: Annotated[dict, Depends(validate_token)]) -> User:
    """
    Check if the current user is the admin
    """

    if str(user.get("id")) != str(ADMIN_TG_ID):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Admin Only",
        )
    
    return user

@app.get("/")
async def index(user: Annotated[dict, Depends(admin_only)]):
    return {"message": user.get("id")}
