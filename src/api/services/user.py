from datetime import datetime
from typing import Type

from api.schemas.create import CreateUserSchema
from config import settings
from database import UserOrm
from fastapi import HTTPException
from pytz import timezone
from security import Hasher
from sqlalchemy import Result
from sqlalchemy import select
from sqlalchemy.exc import DatabaseError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from utils.access_models import PortalAccess


class UserService:
    async def create_user(
        self, user_schema: CreateUserSchema, session: AsyncSession
    ) -> UserOrm:
        async with session.begin():
            user = UserOrm(
                login=user_schema.login,
                email=user_schema.email.__str__(),
                registration_date=datetime.now(timezone(settings.TIMEZONE)).replace(
                    tzinfo=None
                ),
                access_level=PortalAccess.USER,
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

    async def get_user_by_email(self, email, session: AsyncSession) -> UserOrm:
        q = select(UserOrm).filter(UserOrm.email == email)
        async with session.begin():
            user: Result = await session.execute(q)
            return user.scalar()

    async def get_user_by_login(self, login, session: AsyncSession) -> UserOrm:
        q = select(UserOrm).filter(UserOrm.login == login)
        async with session.begin():
            user: Result = await session.execute(q)
            return user.scalar()

    async def get_user_by_id(self, user_id, session: AsyncSession) -> Type[UserOrm]:
        async with session.begin():
            user = await session.get(UserOrm, user_id)
            return user
