from typing import Annotated

import jwt
from config import settings
from database import get_session
from database import UserOrm
from fastapi import Depends
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError
from security import Hasher
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from .user import UserService

user_service = UserService()


class AuthService:

    oauth_scheme = OAuth2PasswordBearer(tokenUrl="/login/")

    @staticmethod
    async def authenticate(login, password, session: AsyncSession) -> UserOrm | bool:
        if "@" in login:
            user = await user_service.get_user_by_email(login, session)
        else:
            user = await user_service.get_user_by_login(login, session)
        if not user:
            return False
        if not Hasher.validate_password(password, user.hpass):
            return False
        return user

    async def get_current_user(
        self,
        token: Annotated[str, Depends(oauth_scheme)],
        session: AsyncSession = Depends(get_session),
    ) -> UserOrm | None:
        """
        Dependency for JWT validation and authorization
        :param token:
        :param session:
        :return:
        """
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
            )
            user_id = payload.get("user_id")
            if user_id is None:
                raise credentials_exception
        except InvalidTokenError:
            raise credentials_exception
        user = await user_service.get_user_by_id(user_id, session)
        if not user:
            raise credentials_exception
        return user
