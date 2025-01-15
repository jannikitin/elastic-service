from api.schemas.create import CreateServiceSchema
from api.schemas.create import CreateUserSchema
from api.schemas.read import ShowUser
from api.services import auth_service
from api.services import user_service
from config import settings
from database import get_session
from database import UserOrm
from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from utils.access_models import CRUDOperation
from utils.access_models import PortalAccess

user_router = APIRouter()


@user_router.post(
    "/registration/",
    status_code=status.HTTP_201_CREATED,
    summary="New user registration",
    description="Accepts new user login, email and password",
    response_model=ShowUser,
)
async def register_user(
    user_schema: CreateUserSchema, session: AsyncSession = Depends(get_session)
):
    user = await user_service.create_user(user_schema, session)
    return ShowUser(id=user.id, email=user.email, login=user.login)


@user_router.get(
    "/me/",
    status_code=status.HTTP_200_OK,
    summary="Get current user data",
    response_model=ShowUser,
)
async def get_me(current_user: UserOrm = Depends(auth_service.get_current_user)):
    return ShowUser(
        id=current_user.id,
        login=current_user.login,
        email=current_user.email,
        name=current_user.name,
        lastname=current_user.lastname,
    )


@user_router.post("/service/", status_code=status.HTTP_201_CREATED)
async def create_service(
    service_data: CreateServiceSchema, session: AsyncSession = Depends(get_session)
):
    if service_data.key != settings.SECRET_KEY:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    user = await user_service.create_user(
        service_data, session, access=PortalAccess.SERVICE
    )
    return {"message": "success", "login": user.login}


@user_router.delete(
    "/{user_id}/",
    status_code=status.HTTP_200_OK,
    summary="Deactivate user to unable login",
)
async def delete_user(
    user_id: str,
    session: AsyncSession = Depends(get_session),
    current_user: UserOrm = Depends(auth_service.get_current_user),
):
    user_to_delete = await user_service.get_user_by_id(user_id, session)
    if (
        await auth_service.verify(user_to_delete, current_user, {CRUDOperation.DELETE})
        is False
    ):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")

    user_id = await user_service.delete_user(user_to_delete, session)
    return {"message": "User deleted", "user_id": user_id.__str__()}
