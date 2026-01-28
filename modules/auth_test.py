from fastapi import FastAPI
from config.settings import settings
from jose import jwt
from datetime import datetime, timedelta


def get_token(user_id: str):
    return {
        "token": create_test_token(user_id)
    }

# ======================
# TESTING ONLY
# REMOVE IN PRODUCTION
# ======================
def create_test_token(user_id: str):
    """
    Generate JWT for local testing only.
    Remove this in production.
    """
    payload = {
        "sub": user_id,
        "exp": datetime.utcnow() + timedelta(days=1),
        "iat": datetime.utcnow()
    }

    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
