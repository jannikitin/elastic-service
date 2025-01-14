from api.schemas.create import CreateUserSchema
from api.schemas.read import ShowUser
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
