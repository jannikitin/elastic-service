from uuid import UUID

from api.authorization import AuthorizationSystem
from api.schemas.create import CreateCompanySchema
from api.schemas.read import ShowCompany
from api.schemas.read import ShowNewMember
from api.services import auth_service
from api.services import company_service
from database import get_session
from database import UserOrm
from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from utils.access_models import InviteRole

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
    AuthorizationSystem.can_create_company(current_user, company_schema)
    company = await company_service.register_company(
        company_schema, current_user, session
    )
    return ShowCompany(
        id=company.id,
        name=company.name,
        owner_id=company.owner_id,
    )


@company_router.get(
    "/{company_id}/",
    status_code=status.HTTP_200_OK,
    summary="Get a company by id",
    response_model=ShowCompany,
)
async def get_company(
    company_id: str,
    current_user: UserOrm = Depends(auth_service.get_current_user),
    session: AsyncSession = Depends(get_session),
):

    company = await company_service.get_company_by_id(company_id, session)
    AuthorizationSystem.can_read_company(current_user, company)
    return ShowCompany(
        id=company.id,
        name=company.name,
        owner_id=company.owner_id,
    )


@company_router.post(
    "/invite/{user_email}/",
    status_code=status.HTTP_201_CREATED,
    summary="Invite user to company with role and by email",
    response_model=ShowNewMember,
)
async def invite_member(
    user_email: EmailStr,
    member_role: InviteRole,
    company_id: UUID,
    current_user: UserOrm = Depends(auth_service.get_current_user),
    session: AsyncSession = Depends(get_session),
):
    company = await company_service.get_company_by_id(company_id, session)
    if not company:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Company not found")
    AuthorizationSystem.can_invite_members(current_user, company)

    employee = await company_service.invite_member(
        user_email, member_role, company, session
    )
    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with {user_email} email not found",
        )
    return ShowNewMember(
        user_id=employee.user_id,
        name=employee.user.name,
        role=employee.role,
        took_office_date=employee.took_office_date,
        company_id=employee.company_id,
    )
