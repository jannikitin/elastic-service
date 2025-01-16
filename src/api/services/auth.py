from typing import Annotated
from typing import Type

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
from utils.access_models import PortalAccess

from .user import UserService

user_service = UserService()


class AuthenticationService:

    oauth_scheme = OAuth2PasswordBearer(tokenUrl="/login/")

    @staticmethod
    async def authenticate(login, password, session: AsyncSession) -> UserOrm | bool:
        if "@" in login:
            user = await user_service.get_user_by_email(login, session)
        else:
            user = await user_service.get_user_by_login(login, session)
        if not user or user.is_active is False:
            return False
        if not Hasher.validate_password(password, user.hpass):
            return False
        return user

    @staticmethod
    async def get_current_user(
        token: Annotated[str, Depends(oauth_scheme)],
        session: AsyncSession = Depends(get_session),
    ) -> Type[UserOrm] | None:
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
        try:
            user = await user_service.get_user_by_id(user_id, session)
        except HTTPException:
            raise credentials_exception
        if not user or user.is_active == False:
            raise credentials_exception
        return user

    @staticmethod
    async def get_current_admin(user: UserOrm = Depends(get_current_user)):
        user = await user
        if user.access_level is PortalAccess.USER:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden"
            )
        return user
