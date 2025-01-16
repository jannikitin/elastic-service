from uuid import UUID

from api.authorization import AuthorizationSystem
from api.schemas.create import CreateUserSchema
from api.schemas.read import ShowUserSchema
from api.schemas.update import UserUpdateSchema
from api.services import auth_service
from api.services import user_service
from database import get_session
from database import UserOrm
from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

user_router = APIRouter()


@user_router.post(
    "/registration/",
    status_code=status.HTTP_201_CREATED,
    summary="New user registration",
    description="Accepts new user login, email and password",
    response_model=ShowUserSchema,
)
async def register_user(
    user_schema: CreateUserSchema, session: AsyncSession = Depends(get_session)
):
    user = await user_service.create_user(user_schema, session)
    return ShowUserSchema(id=user.id, email=user.email, login=user.login)


@user_router.get(
    "/me/",
    status_code=status.HTTP_200_OK,
    summary="Get current user data",
    response_model=ShowUserSchema,
)
async def get_me(current_user: UserOrm = Depends(auth_service.get_current_user)):
    return ShowUserSchema(
        id=current_user.id,
        login=current_user.login,
        email=current_user.email,
        name=current_user.name,
        lastname=current_user.lastname,
    )


@user_router.delete(
    "/{user_id}/",
    status_code=status.HTTP_200_OK,
    summary="Deactivate user to unable login",
)
async def delete_user(
    user_id: UUID,
    session: AsyncSession = Depends(get_session),
    current_user: UserOrm = Depends(auth_service.get_current_user),
):
    user_to_delete = await user_service.get_user_by_id(user_id, session)
    AuthorizationSystem.can_delete_user(current_user, user_to_delete)

    user_id = await user_service.delete_user(user_to_delete, session)
    return {"message": "User deleted", "user_id": user_id.__str__()}


@user_router.patch(
    "/{user_id}/",
    status_code=status.HTTP_200_OK,
    summary="Update user public data",
    response_model=ShowUserSchema,
)
async def update_user(
    user_id: UUID,
    body: UserUpdateSchema,
    session: AsyncSession = Depends(get_session),
    current_user: UserOrm = Depends(auth_service.get_current_user),
):
    user_to_update = await user_service.get_user_by_id(user_id, session)
    AuthorizationSystem.can_update_user(current_user, user_to_update)
    updated_user = await user_service.update_user(user_to_update, body, session)
    return ShowUserSchema(
        login=updated_user.login,
        email=updated_user.email,
        name=updated_user.name,
        lastname=updated_user.lastname,
    )


@user_router.get(
    "/{user_id}/",
    status_code=status.HTTP_200_OK,
    summary="Get public user data",
    response_model=ShowUserSchema,
)
async def get_public_user(user_id: UUID, session: AsyncSession = Depends(get_session)):
    user = await user_service.get_user_by_id(user_id, session)
    return ShowUserSchema(
        login=user.login, email=user.email, name=user.name, lastname=user.lastname
    )
