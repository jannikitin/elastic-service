from api.schemas.create import CreateCompanySchema
from api.schemas.read import ShowCompany
from api.services import auth_service
from database import get_session
from database import UserOrm
from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

company_router = APIRouter()


@company_router.post(
    "/registration/",
    status_code=status.HTTP_201_CREATED,
    summary="Create a new company and register user under user_id field as owner of this company",
    response_model=ShowCompany,
)
async def create_company(
    company_schema: CreateCompanySchema,
    session: AsyncSession = Depends(get_session),
    current_user: UserOrm = Depends(auth_service.get_current_user),
):
    pass


@company_router.get("/{company_id}/")
async def get_company(company_id: str):
    pass
