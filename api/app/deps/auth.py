from fastapi import Depends, HTTPException
from fastapi.security import (HTTPBearer, HTTPAuthorizationCredentials,
                              APIKeyHeader)
from starlette import status
from typing import Optional
import jwt

from ..globals import JWT_SECRET, JWT_ALGORITHM, ADMIN_TG_ID, BOT_API_KEY
from schemas import UserAuthSchema, Role

api_key_header = APIKeyHeader(name="x-api-key", auto_error=False)
http_bearer = HTTPBearer(auto_error=False)

async def get_current_user(
    api_key: Optional[str] = Depends(api_key_header),
    token: Optional[HTTPAuthorizationCredentials] = Depends(http_bearer)
) -> UserAuthSchema:
    """
    Get the current user from either API Key or JWT
    """

    if api_key:
        if api_key == BOT_API_KEY:
            # Authorization is handled on the bot side, so the bot itself has
            # admin privileges
            return UserAuthSchema(
                tg_id=ADMIN_TG_ID,
                role=Role.ADMIN,
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid API Key",
            )
    
    if token:
        try:
            payload = jwt.decode(
                token.credentials, 
                JWT_SECRET, 
                algorithms=[JWT_ALGORITHM],
                options={"require": ["exp", "sub"]}
            )
            return UserAuthSchema(
                tg_id=payload.get("sub"),
                role=(
                    Role.ADMIN if payload.get("sub") == ADMIN_TG_ID
                    else Role.USER
                ),
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
    
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Not authenticated",
    )

# https://medium.com/@bhagyarana80/how-i-built-a-role-based-access-control-system-with-fastapi-and-pydantic-2c49e967efb0
def authorize_current_user(allowed_roles: list[Role]):
    def wrapper(
        user: UserAuthSchema = Depends(get_current_user)
    ) -> UserAuthSchema:
        if user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied for role: {user.role}"
            )
        return user
    return wrapper
