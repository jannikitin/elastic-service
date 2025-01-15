from datetime import datetime
from functools import wraps
from typing import Type

from api.schemas.create import CreateUserSchema
from api.schemas.update import UserUpdateSchema
from config import settings
from database import UserOrm
from fastapi import HTTPException
from pytz import timezone
from security import Hasher
from sqlalchemy import Result
from sqlalchemy import select
from sqlalchemy import update
from sqlalchemy.exc import DatabaseError
from sqlalchemy.exc import DBAPIError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from utils.access_models import PortalAccess


class UserService:
    @staticmethod
    def not_found(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            not_found_ex = HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )
            try:
                result = await func(*args, **kwargs)
            except DBAPIError:
                raise not_found_ex
            else:
                if result is None:
                    raise not_found_ex
            return result

        return wrapper

    async def create_user(
        self,
        user_schema: CreateUserSchema,
        session: AsyncSession,
        access: PortalAccess = PortalAccess.USER,
    ) -> UserOrm:
        async with session.begin():
            user = UserOrm(
                login=user_schema.login,
                email=user_schema.email.__str__(),
                registration_date=datetime.now(timezone(settings.TIMEZONE)).replace(
                    tzinfo=None
                ),
                access_level=access,
                hpass=Hasher.get_hashed_password(user_schema.password),
                is_active=True,
            )
            session.add(user)
            try:
                await session.flush()
            except DatabaseError:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="User is already registered",
                )
            return user

    @not_found
    async def get_user_by_email(self, email, session: AsyncSession) -> UserOrm:
        q = select(UserOrm).filter(UserOrm.email == email)
        async with session.begin():
            user: Result = await session.execute(q)
            return user.scalar()

    @not_found
    async def get_user_by_login(self, login, session: AsyncSession) -> UserOrm:
        q = select(UserOrm).filter(UserOrm.login == login)
        async with session.begin():
            user: Result = await session.execute(q)
            return user.scalar()

    @not_found
    async def get_user_by_id(self, user_id, session: AsyncSession) -> Type[UserOrm]:
        async with session.begin():
            user = await session.get(UserOrm, user_id)
            return user

    async def delete_user(self, user: UserOrm, session: AsyncSession):
        if user.is_active is False:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User is already unregistered",
            )

        q = (
            update(UserOrm)
            .where(UserOrm.id == user.id)
            .values({"is_active": False})
            .returning(UserOrm.id)
        )
        async with session.begin():
            res: Result = await session.execute(q)
            return res.one()[0]

    async def grant_admin_access(self, user: UserOrm, session: AsyncSession):
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User is unactive",
            )

        if user.access_level in {PortalAccess.ADMIN, PortalAccess.SERVICE}:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User is already granted",
            )

        q = (
            update(UserOrm)
            .filter(UserOrm.id == user.id)
            .values({"access_level": PortalAccess.ADMIN})
            .returning(UserOrm.id)
        )
        async with session.begin():
            res: Result = await session.execute(q)
            return res.one()[0]

    async def activate_user(self, user: UserOrm, session: AsyncSession):
        if user.is_active is True:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User is already active",
            )

        q = (
            update(UserOrm)
            .filter(UserOrm.id == user.id)
            .values({"is_active": True})
            .returning(UserOrm.id)
        )
        async with session.begin():
            res: Result = await session.execute(q)
            return res.one()[0]

    async def remove_admin_access(self, user: UserOrm, session: AsyncSession):
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User is unactive",
            )

        if user.access_level is PortalAccess.SERVICE:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User is service account",
            )
        elif user.access_level is PortalAccess.USER:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User have no permission yet",
            )

        q = (
            update(UserOrm)
            .filter(UserOrm.id == user.id)
            .values({"access_level": PortalAccess.USER})
            .returning(UserOrm.id)
        )

        async with session.begin():
            res: Result = await session.execute(q)
            return res.one()[0]

    async def update_user(
        self, user: UserOrm, schema: UserUpdateSchema, session: AsyncSession
    ):
        async with session.begin():
            session.add(user)
            for key, value in schema.model_dump().items():
                setattr(user, key, value)
            await session.flush()
            return user
