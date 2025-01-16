from api.authorization import AuthorizationSystem
from api.exc import forbidden_exception
from api.schemas.create import CreateServiceSchema
from api.schemas.read import ShowUserSchema
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
from utils.access_models import PortalAccess

admin_router = APIRouter()


@admin_router.post("/service/", status_code=status.HTTP_201_CREATED)
async def create_service(
    service_data: CreateServiceSchema, session: AsyncSession = Depends(get_session)
):
    if service_data.key != settings.SECRET_KEY:
        raise forbidden_exception
    user = await user_service.create_user(
        service_data, session, access=PortalAccess.SERVICE
    )
    return {"message": "success", "login": user.login}


@admin_router.patch(
    "/service/grant/{user_id}/",
    status_code=status.HTTP_200_OK,
    summary="Grant admin access to user",
)
async def grant_admin_access(
    user_id: str,
    session: AsyncSession = Depends(get_session),
    admin: UserOrm = Depends(auth_service.get_current_admin),
):
    user = await user_service.get_user_by_id(user_id, session)
    user_id = await user_service.grant_admin_access(user, session)
    if user_id:
        return ShowUserSchema(
            id=user.id,
            login=user.login,
            email=user.email,
            name=user.name,
            lastname=user.lastname,
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User is not updated"
        )


@admin_router.patch(
    "/service/remove/{user_id}/",
    status_code=status.HTTP_200_OK,
    summary="Remove admin access",
)
async def remove_admin_access(
    user_id: str,
    session: AsyncSession = Depends(get_session),
    admin: UserOrm = Depends(auth_service.get_current_admin),
):
    user = await user_service.get_user_by_id(user_id, session)
    AuthorizationSystem.can_remove_admin_access(admin, user)
    user_id = await user_service.remove_admin_access(user, session)

    if user_id:
        return ShowUserSchema(
            id=user.id,
            login=user.login,
            email=user.email,
            name=user.name,
            lastname=user.lastname,
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User is not updated"
        )


@admin_router.patch(
    "/activate/{user_id}/", status_code=status.HTTP_200_OK, summary="Activate user"
)
async def activate_user(
    user_id: str,
    session: AsyncSession = Depends(get_session),
    admin: UserOrm = Depends(auth_service.get_current_admin),
):

    user = await user_service.get_user_by_id(user_id, session)
    AuthorizationSystem.can_update(admin, user)
    user_id = await user_service.activate_user(user, session)
    if user_id:
        return ShowUserSchema(
            id=user.id,
            login=user.login,
            email=user.email,
            name=user.name,
            lastname=user.lastname,
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User is not updated"
        )
