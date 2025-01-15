import asyncio
import os
import subprocess
from typing import List

import httpx
import pytest
from api.schemas.create import CreateUserSchema
from database import Base
from database import get_session
from database import UserOrm
from main import app
from security import create_jwt_token
from sqlalchemy import text
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from utils.access_models import PortalAccess

engine = create_async_engine(
    "postgresql+asyncpg://"
    "postgres_test:postgres_test@localhost:5001/"
    "postgres_test?async_fallback=True",
    echo=False,
    future=True,
)
session_factory = async_sessionmaker(
    bind=engine, expire_on_commit=False, class_=AsyncSession
)


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session", autouse=True)
def run_migrations():
    project_root = os.path.abspath(
        os.path.dirname(__file__)
    )  # Основная директория проекта
    migrations_path = os.path.join(project_root, "migrations")
    alembic_ini_path = os.path.join(project_root, "alembic.ini")

    # Убедитесь, что папка для миграций существует
    os.makedirs(migrations_path, exist_ok=True)

    # Инициализация Alembic, если папка migrations пуста
    if not os.listdir(migrations_path):
        subprocess.run(
            ["alembic", "init", migrations_path], cwd=project_root, check=True
        )

    # Применение миграций
    subprocess.run(
        ["alembic", "-c", alembic_ini_path, "upgrade", "heads"],
        cwd=project_root,
        check=True,
    )


async def get_test_session():
    session = session_factory()
    try:
        yield session
    finally:
        await session.close()


@pytest.fixture(scope="function")
async def client():
    app.dependency_overrides[get_session] = get_test_session
    async with httpx.AsyncClient(
        base_url="http://0.0.0.0", transport=httpx.ASGITransport(app=app)
    ) as client:
        yield client


@pytest.fixture(scope="function", autouse=True)
async def clear_data():
    async with session_factory() as session:
        async with session.begin():
            for table in Base.metadata.tables.keys():
                await session.execute(text(f"TRUNCATE TABLE public.{table} CASCADE"))


@pytest.fixture(scope="function")
async def valid_user() -> CreateUserSchema:
    return CreateUserSchema(
        login="test_login", password="12345678Aa", email="test@example.com"
    )


def get_token(user_id):
    token = create_jwt_token(data={"user_id": user_id.__str__()})
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture(scope="function")
async def create_admins() -> List[str]:
    """
    returns admin_id, service_id
    """
    async with session_factory() as session:
        async with session.begin():
            admin = UserOrm(
                login="admin",
                email="admin@example.com",
                hpass="12345678Aa",
                access_level=PortalAccess.ADMIN,
            )
            service = UserOrm(
                login="service",
                email="service@example.com",
                hpass="12345678Aa",
                access_level=PortalAccess.SERVICE,
            )
            session.add_all([admin, service])
            await session.flush()

        return [admin.id.__str__(), service.id.__str__()]
