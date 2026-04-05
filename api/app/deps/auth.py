from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from starlette import status
from typing import Annotated
import jwt

from ..globals import JWT_SECRET, JWT_ALGORITHM, ADMIN_TG_ID
from ..schemas import UserId

http_bearer = HTTPBearer()

async def validate_token(
    auth: Annotated[HTTPAuthorizationCredentials, Depends(http_bearer)]
) -> UserId:
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
    
    return UserId(tg_id=payload.get("sub"))

async def admin_only(user: Annotated[UserId, Depends(validate_token)]) -> UserId:
    """
    Check if the current user is the admin
    """

    if user.tg_id != ADMIN_TG_ID:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Admin Only",
        )
    
    return user