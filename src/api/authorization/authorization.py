from api.schemas.create import CreateCompanySchema
from api.services import company_service
from database import UserOrm
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from .handlers import CanDeleteUser
from .handlers import CanReadUser
from .handlers import CanRemoveAdminAccess
from .handlers import CanUpdateUser


class AuthorizationSystem:
    @staticmethod
    def can_delete(user: UserOrm, target: UserOrm):
        verificator = CanDeleteUser()
        verificator.validate(user, target)

    @staticmethod
    def can_read(user: UserOrm, target: UserOrm):
        verificator = CanReadUser()
        verificator.validate(user, target)

    @staticmethod
    def can_update(user: UserOrm, target: UserOrm):
        verificator = CanUpdateUser()
        verificator.validate(user, target)

    @staticmethod
    def can_remove_admin_access(user: UserOrm, target: UserOrm):
        verificator = CanRemoveAdminAccess()
        verificator.validate(user, target)

    @staticmethod
    async def can_create_company(
        user: UserOrm, company_schema: CreateCompanySchema, session: AsyncSession
    ):
        # is company member -> is company under user id
        company = await company_service.get_employee_company_id(user.id, session)
        if company:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Employee already member of the company"
                f"{company.company_name}",
            )
        if user.id.__str__() != company_schema.owner_id:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"User {user.id} is not the owner of the specified company",
            )
