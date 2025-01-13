import uuid
from datetime import datetime
from typing import Annotated

from config import settings
from sqlalchemy import DateTime
from sqlalchemy import func
from sqlalchemy import Integer
from sqlalchemy import UUID
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import mapped_column


engine = create_async_engine(settings.postgres_url())
sessionmaker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


pk_uuid = Annotated[
    uuid.UUID, mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
]
pk_int = Annotated[int, mapped_column(Integer, primary_key=True, autoincrement=True)]
created_at = Annotated[datetime, mapped_column(DateTime, server_default=func.now())]


class Base(DeclarativeBase):
    pass
