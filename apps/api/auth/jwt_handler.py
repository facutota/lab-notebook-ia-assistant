from datetime import timedelta, datetime, UTC
from typing import Any, Dict, List
from jose import jwt

from config import settings


def create_access_token(subject: str, roles: List[str], expires_in: timedelta) -> str:
    expiration = datetime.now(UTC) + expires_in
    to_encode = {
        "sub": str(subject),
        "exp": expiration,
        "iat": datetime.now(UTC),
        "roles": roles,
    }

    encoded_jwt = jwt.encode(to_encode, settings.auth_secret_key, algorithm=settings.algorithm)

    return encoded_jwt


def create_refresh_token(subject: str) -> str:
    expiration = datetime.now(UTC) + timedelta(days=settings.refresh_token_expire_in_days)
    to_encode = {
        "sub": str(subject),
        "exp": expiration,
        "iat": datetime.now(UTC),
        "token_type": "refresh",
    }
    encoded_jwt = jwt.encode(to_encode, settings.auth_secret_key, algorithm=settings.algorithm)
    return encoded_jwt


def decode_token(token: str) -> Dict[str, Any]:
    payload = jwt.decode(token, settings.auth_secret_key, algorithms=[settings.algorithm])
    return payload
