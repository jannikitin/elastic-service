from datetime import datetime
from datetime import timedelta
from datetime import UTC

import jwt
from config import settings
from passlib.context import CryptContext

crypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Hasher:
    @staticmethod
    def get_hashed_password(password):
        return crypt_context.hash(password)

    @staticmethod
    def validate_password(password, hashed_password):
        return crypt_context.verify(password, hashed_password)


def create_jwt_token(data: dict, exp: timedelta = None):
    payload = data.copy()
    if exp:
        expire = datetime.now(UTC) + exp
    else:
        expire = datetime.now(UTC) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

    payload.update({"exp": expire})
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return token
