from api.schemas.create import CreateCompanySchema
from database import CompanyOrm
from database import UserOrm
from fastapi import HTTPException
from starlette import status

from .handlers import CanDeleteUser
from .handlers import CanInvite
from .handlers import CanPerform
from .handlers import CanReadUser
from .handlers import CanRemoveAdminAccess
from .handlers import CanUpdateUser
from .handlers import IsCompanyMember
from .handlers import IsEmployee


class AuthorizationSystem:
    @staticmethod
    def can_delete_user(user: UserOrm, target: UserOrm):
        verificator = CanDeleteUser()
        verificator.validate(user, target)

    @staticmethod
    def can_read_user(user: UserOrm, target: UserOrm):
        verificator = CanReadUser()
        verificator.validate(user, target)

    @staticmethod
    def can_update_user(user: UserOrm, target: UserOrm):
        verificator = CanUpdateUser()
        verificator.validate(user, target)

    @staticmethod
    def can_remove_admin_access(user: UserOrm, target: UserOrm):
        verificator = CanRemoveAdminAccess()
        verificator.validate(user, target)

    @staticmethod
    async def can_create_company(user: UserOrm, company_schema: CreateCompanySchema):
        # is company member -> is company under user id
        if user.employee:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Employee already member of the company"
                f"{user.employee.company_id}",
            )
        if user.id.__str__() != company_schema.owner_id:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"User {user.id} is not the owner of the specified company",
            )

    @staticmethod
    def can_read_company(user: UserOrm, company: CompanyOrm):
        verificator = CanPerform(IsEmployee(IsCompanyMember()))
        verificator.validate(user, target=company)

    @staticmethod
    def can_invite_members(user: UserOrm, company: CompanyOrm):
        verificator = CanPerform(IsEmployee(IsCompanyMember(CanInvite())))
        verificator.validate(user, target=company)
