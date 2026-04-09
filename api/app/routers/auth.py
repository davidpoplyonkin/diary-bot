from fastapi import APIRouter, HTTPException, Header
from starlette import status
from typing import Annotated
import hashlib
import hmac
import jwt
from urllib.parse import parse_qsl
import json
from datetime import datetime, timezone, timedelta
from time import time

from schemas import TokenSchema
from ..globals import TG_TOKEN, JWT_SECRET, JWT_ALGORITHM, JWT_EXP_SECONDS

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)

@router.post("/token", response_model=TokenSchema)
async def issue_token(
    x_telegram_init_data: Annotated[str, Header()]
) -> TokenSchema:
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
    
    return TokenSchema(
        access_token=token,
        token_type="bearer"
    )
