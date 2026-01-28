from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer
from jose import jwt, JWTError
from config.settings import settings


security = HTTPBearer()


def get_current_user(token=Depends(security)):

    try:

        payload = jwt.decode(
            token.credentials,
            settings.SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM]
        )

        user_id = payload.get("sub")

        if not user_id:
            raise JWTError

        return user_id

    except:

        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )
