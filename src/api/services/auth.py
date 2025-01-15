from abc import ABC
from abc import abstractmethod
from typing import Annotated
from typing import Final
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
from sqlalchemy.exc import DBAPIError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from utils.access_models import CRUDOperation
from utils.access_models import PortalAccess

from .user import UserService

user_service = UserService()


class BaseAccessVerificator(ABC):

    ALL: Final[set[CRUDOperation]] = {
        CRUDOperation.READ,
        CRUDOperation.DELETE,
        CRUDOperation.UPDATE,
        CRUDOperation.CREATE,
    }
    NON_DELETE_ALL: Final[set[CRUDOperation]] = ALL - {CRUDOperation.DELETE}

    @abstractmethod
    async def verify(
        self, resource, user: UserOrm, operations: set[CRUDOperation]
    ) -> bool:
        raise NotImplementedError()


class VerificationTransfer(BaseAccessVerificator):
    async def verify(
        self, resource, user: UserOrm, operations: set[CRUDOperation]
    ) -> bool:
        if isinstance(resource, UserOrm):
            return await UserRelationVerificator.verify(resource, user, operations)


class UserRelationVerificator(BaseAccessVerificator):

    ACCESS_RELATIONS: dict[PortalAccess | str, dict] = {
        PortalAccess.SERVICE: {
            PortalAccess.USER: BaseAccessVerificator.ALL,
            PortalAccess.ADMIN: BaseAccessVerificator.ALL,
            PortalAccess.SERVICE: BaseAccessVerificator.NON_DELETE_ALL,
            "SELF": BaseAccessVerificator.NON_DELETE_ALL,
        },
        PortalAccess.ADMIN: {
            PortalAccess.USER: BaseAccessVerificator.ALL,
            PortalAccess.ADMIN: BaseAccessVerificator.NON_DELETE_ALL,
            PortalAccess.SERVICE: {CRUDOperation.READ},
            "SELF": BaseAccessVerificator.NON_DELETE_ALL,
        },
        PortalAccess.USER: {
            PortalAccess.USER: {CRUDOperation.READ},
            PortalAccess.ADMIN: {},
            PortalAccess.SERVICE: {},
            "SELF": BaseAccessVerificator.NON_DELETE_ALL,
        },
    }

    @classmethod
    async def verify(
        cls, resource: UserOrm, user: UserOrm, operations: set[CRUDOperation]
    ) -> bool:
        access_level_table = cls.ACCESS_RELATIONS.get(user.access_level, {})
        if resource.id == user.id:
            permissions = access_level_table.get("SELF", {})
        else:
            permissions = access_level_table.get(resource.access_level, {})
        if not operations.issubset(permissions):
            return False
        return True


class AuthService(VerificationTransfer):

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

    async def verify(
        self, resource, user: UserOrm, operations: set[CRUDOperation]
    ) -> bool:
        return await super().verify(resource, user, operations)

    async def get_current_user(
        self,
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
        except DBAPIError:
            raise credentials_exception
        if not user or user.is_active == False:
            raise credentials_exception
        return user
