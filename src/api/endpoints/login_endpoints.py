from api.schemas.response import Token
from api.services import auth_service
from database import get_session
from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from security import create_jwt_token
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

login_router = APIRouter()


@login_router.post("/", status_code=status.HTTP_200_OK, response_model=Token)
async def login(
    login_schema: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_session),
):
    user = await auth_service.authenticate(
        login_schema.username, login_schema.password, session
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    payload = {"user_id": user.id.__str__()}

    token = create_jwt_token(payload)
    return Token(access_token=token, token_type="Bearer")
